from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pydantic import BaseModel
from pathlib import Path
import os
from dotenv import load_dotenv
from google import genai
import pymupdf
from google.genai import types
import faiss
import numpy as np

app = FastAPI(title="Document Q&A Assistant")

vector_db=None
document_chunks=[]

load_dotenv()
client=genai.Client(
    api_key=os.getenv("MODEL_NAME"))

model="gemini-embedding-2"

# ==============================
# CORS
# ==============================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ==============================
# Upload folder
# ==============================

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB


# ==============================
# Pydantic Model
# ==============================

class ContentRequest(BaseModel):
    content: str



class QuestionRequest(BaseModel):
    question:str


# ==============================
# PDF Text Extraction
# ==============================

def extract_pdf_text(file_path):

    document = pymupdf.open(file_path)

    text = ""

    for page_number, page in enumerate(document):

        page_text = page.get_text()

        text += f"\n[Page {page_number + 1}]\n"
        text += page_text

    document.close()

    return text


# ==============================
# TXT Text Extraction
# ==============================

def extract_txt_text(file_path):

    with open(
        file_path,
        "r",
        encoding="utf-8"
    ) as file:

        return file.read()


# ==============================
# Text Cleaning
# ==============================

def clean_text(text):

    text = text.replace("\n", " ")

    text = " ".join(text.split())

    return text.strip()


# ==============================
# UPLOAD API
# ==============================

@app.post("/upload")
async def upload_file(
    file: UploadFile = File(...)
):

    # File name check

    if not file.filename:

        raise HTTPException(
            status_code=400,
            detail="No file selected"
        )


    filename = file.filename.lower()


    # Extension validation

    if not (
        filename.endswith(".pdf")
        or filename.endswith(".txt")
    ):

        raise HTTPException(
            status_code=400,
            detail="Only PDF and TXT files are allowed"
        )


    # Read file

    content = await file.read()


    # Empty file

    if len(content) == 0:

        raise HTTPException(
            status_code=400,
            detail="File is empty"
        )


    # Size validation

    if len(content) > MAX_FILE_SIZE:

        raise HTTPException(
            status_code=400,
            detail="File must be less than 10 MB"
        )


    # Save file

    file_path = UPLOAD_DIR / file.filename

    with open(file_path, "wb") as f:

        f.write(content)


    # ==========================
    # Extract text
    # ==========================

    if filename.endswith(".pdf"):

        extracted_text = extract_pdf_text(
            file_path
        )

    else:

        extracted_text = extract_txt_text(
            file_path
        )


    # Clean text
    cleaned_text=clean_text(extracted_text)


    if not cleaned_text:

        raise HTTPException(
            status_code=400,
            detail="No readable text found in document"
        )

    global vector_db
    global document_chunks
    chunks=create_chunks(cleaned_text)

    embeddings=generate_embeddings(chunks)

    index=create_vector_database(chunks,embeddings)

    return {

        "success": True,

        "message": "Document uploaded successfully",

        "filename": file.filename,

        "text_length": len(cleaned_text),

        "chunk_count":len(chunks),

        "embedding_count":len(embeddings),

        "vectors_in_database":index.ntotal,

    }


# ==============================
# PASTE CONTENT API
# ==============================
@app.post("/content")
async def receive_content(data: ContentRequest):

    global vector_db
    global document_chunks

    content = data.content.strip()

    # Content validation
    if not content:
        raise HTTPException(
            status_code=400,
            detail="Document content cannot be empty"
        )

    # Clean content
    cleaned_content = clean_text(content)

    # Create chunks
    chunks = create_chunks(cleaned_content)

    if not chunks:
        raise HTTPException(
            status_code=400,
            detail="Could not create document chunks"
        )

    # Generate embeddings
    embeddings = generate_embeddings(chunks)

    # Create FAISS database
    index = create_vector_database(
        chunks,
        embeddings
    )

    return {
        "success": True,
        "message": "Content stored successfully",
        "chunks": len(chunks),
        "embeddings": len(embeddings),
        "vectors_in_database": index.ntotal
    }

@app.post("/ask")
async def ask_question(data: QuestionRequest):

    global vector_db
    global document_chunks

    # =========================
    # Get Question
    # =========================

    question = data.question.strip()

    if not question:
        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty"
        )

    # =========================
    # Check Document
    # =========================

    if vector_db is None:
        raise HTTPException(
            status_code=400,
            detail="Please upload PDF or paste content first"
        )

    if document_chunks is None or len(document_chunks) == 0:
        raise HTTPException(
            status_code=400,
            detail="No document content available"
        )

    # =========================
    # Search Relevant Chunks
    # =========================

    results = search_similar_chunks(
        question,
        top_k=3
    )

    if not results:
        return {
            "success": True,
            "question": question,
            "answer": "I could not find the answer in the provided document.",
            "results": [],
            "source_context": ""
        }

    # =========================
    # Create Context
    # =========================

    context = "\n\n".join(
        result["chunk"]
        for result in results
    )

    # =========================
    # Generate Answer
    # =========================

    answer = generate_answer(
        question,
        context
    )

    # =========================
    # Return Response
    # =========================

    return {
        "success": True,
        "question": question,
        "answer": answer,
        "results": results,
        "source_context": context
    }

def create_chunks(text):

    text_splitter=RecursiveCharacterTextSplitter(
        separators=["\n\n","\n","."," "],
        chunk_size=1000,
        chunk_overlap=200
    )
    chunks=text_splitter.split_text(text)
    return chunks

def generate_embeddings(chunks):
    contents=[
        types.Content(
            parts=[
                types.Part.from_text(text=chunk)
            ]
        )
        for chunk in chunks
    ]
    result=client.models.embed_content(
            model="gemini-embedding-2",
            contents=contents
        )
    embeddings=[
            embedding.values 
            for embedding in result.embeddings]
    return embeddings




def create_vector_database(chunks,embeddings):
    global vector_db
    global document_chunks

    embedding_array=np.array(
        embeddings,dtype="float32"
    )
    faiss.normalize_L2(embedding_array)
    dimension=embedding_array.shape[1]
    vector_db=faiss.IndexFlatIP(dimension)
    vector_db.add(embedding_array)
    document_chunks=chunks

    return vector_db

def search_similar_chunks(question, top_k=3):

    global vector_db
    global document_chunks

    # Check vector database
    if vector_db is None:
        raise HTTPException(
            status_code=400,
            detail="Please upload a document first"
        )

    # Check chunks
    if document_chunks is None or len(document_chunks) == 0:
        raise HTTPException(
            status_code=400,
            detail="No document chunks available"
        )

    # Question → Embedding
    question_embedding = generate_embeddings(
        [question]
    )[0]

    # Convert to NumPy
    question_vector = np.array(
        [question_embedding],
        dtype="float32"
    )

    # Normalize
    faiss.normalize_L2(question_vector)

    # Number of results
    k = min(top_k, vector_db.ntotal)

    # Similarity search
    scores, indexes = vector_db.search(
        question_vector,
        k
    )

    results = []

    for i, score in zip(
        indexes[0],
        scores[0]
    ):

        if i != -1:

            results.append({
                "chunk": document_chunks[i],
                "score": float(score)
            })

    return results

def generate_answer(question, context):

    if not context:
        return "I could not find the answer in the provided document."

    prompt = f"""
You are a Document Question Answering Assistant.

Your job is to answer the user's question using ONLY
the information provided in the document context.

Rules:

1. Use only the provided document context.
2. Do not use outside knowledge.
3. Do not make up information.
4. Give a clear and simple answer.
5. If the answer is not present in the document, say:
6.summarise the document in which langualge need for user
"I could not find the answer in the provided document."

DOCUMENT CONTEXT:
{context}

USER QUESTION:
{question}

ANSWER:
"""

    try:

        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt
        )

        return response.text

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"Gemini API error: {str(e)}"
        )