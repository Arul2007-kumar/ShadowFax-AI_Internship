from fastapi import APIRouter, UploadFile, File, HTTPException
import os
import shutil
import uuid

from app.ingestion.loaders import load_document
from app.ingestion.cleaner import clean_text
from app.ingestion.chunker import create_chunks
from app.embeddings.service import generate_embeddings
from app.retrieval.store import FAISSStore
from app.graph.nodes import set_vector_store


router = APIRouter(
    prefix="/documents",
    tags=["Ingestion"]
)


UPLOAD_DIR = "data/uploads"

os.makedirs(UPLOAD_DIR, exist_ok=True)


# Global FAISS store
vector_store = None


@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...)
):

    global vector_store

    allowed_extensions = {
        ".pdf",
        ".txt",
        ".md"
    }

    filename = file.filename or ""

    extension = os.path.splitext(
        filename
    )[1].lower()

    if extension not in allowed_extensions:

        raise HTTPException(
            status_code=400,
            detail="Only PDF, TXT and Markdown files are supported."
        )

    document_id = str(uuid.uuid4())

    safe_filename = (
        f"{document_id}_{filename}"
    )

    file_path = os.path.join(
        UPLOAD_DIR,
        safe_filename
    )

    try:

        with open(
            file_path,
            "wb"
        ) as buffer:

            shutil.copyfileobj(
                file.file,
                buffer
            )

        # -------------------------
        # Parsing
        # -------------------------

        pages = load_document(
            file_path
        )

        # -------------------------
        # Cleaning
        # -------------------------

        cleaned_pages = []

        for page in pages:

            cleaned_text = clean_text(
                page["text"]
            )

            cleaned_pages.append({
                **page,
                "text": cleaned_text
            })

        # -------------------------
        # Chunking
        # -------------------------

        # -------------------------
# Cleaning + Chunking
# -------------------------
        for page in cleaned_pages:
    page_chunks = create_chunks(page["text"])

    for chunk in page_chunks:
        all_chunks.append({
            "document_id": document_id,
            "filename": filename,
            "page": page["page"],
            "chunk_id": len(all_chunks),
            "text": chunk
        })
        chunks = all_chunks

        # -------------------------
        # Embeddings
        # -------------------------

        texts = [
            chunk["text"]
            for chunk in chunks
        ]

        embeddings = generate_embeddings(
            texts
        )

        # -------------------------
        # FAISS
        # -------------------------

        vector_store = FAISSStore()

        vector_store.build(
            chunks,
            embeddings
        )

        # Connect to LangGraph

        set_vector_store(
            vector_store
        )

        return {
            "success": True,
            "document_id": document_id,
            "filename": filename,
            "chunks": len(chunks),
            "embeddings": len(embeddings),
            "message": "Document processed successfully."
        }

    except Exception as e:

        if os.path.exists(file_path):
            os.remove(file_path)

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )