from fastapi import FastAPI
from app.schemas.request import QuestionRequest
from app.schemas.response import AnswerResponse
from app.ingestion.loaders import load_document
from app.ingestion.cleaner import clean_text
from app.ingestion.chunker import create_chunks
from app.retrieval.store import FAISSStore
from app.embeddings.service import generate_embeddings
from app.retrieval.query_rewriter import rewrite_query
from app.retrieval.reranker import rerank
from app.generation.llm import generate_grounded_answer
from app.generation.groundedness import (
    check_groundedness,
    build_citations
)
from app.graph.workflow import build_workflow
from app.graph.nodes import set_vector_store
from app.api.routes_ingestion import router as ingestion_router
from app.api.routes_query import router as query_router

app=FastAPI(
    title="produciton Rag assistant",
    description="Ai powered document",
    version="1.0.0"
)


app.include_router(
    ingestion_router
)

app.include_router(
    query_router
)


rag_workflow=build_workflow()

vector_store=FAISSStore()


@app.get("/")
def home():
    return{"message":"production"}

@app.get("/health")
def health_check():
    return{
        "status":"healthy"
    }

@app.post("/test-question")
def test_question(request:QuestionRequest):
    return{
        "question":request.question,
        "document_id":request.document_id,
        "top_k":request.top_k
    }


@app.get("/test-chunking")
def test_chunking():
    file_path="data/sample.txt"
    pages=load_document(file_path)
    all_chunks=[]

    for page in pages:
        cleaned_text=clean_text(page["text"])
        chunks=create_chunks(cleaned_text)

        for chunk_id,chunk in enumerate(chunks):
            all_chunks.append({
                "chunk_id":chunk_id,
                "page":page["page"],
                "text":chunk
            })
    return{
        "total_chunks":len(all_chunks),
        "chunks":all_chunks
    }

@app.get("/test-embedding")
def test_embedding():
    chunks=[
        "machine learning is a branch of artificial intelligence",
        "python is widely used for machine learning"
    ]
    embeddings=generate_embeddings(chunks)

    return{
        "number_of_chunks":len(chunks),
        "number_of_embeddings":len(embeddings),
        "embedding_dimension":len(embeddings[0]) if embeddings else 0

    }

@app.get("/test-faiss")
def test_faiss():

    chunks = [
        {
            "chunk_id": 0,
            "page": 1,
            "text": "Machine learning is a branch of artificial intelligence."
        },
        {
            "chunk_id": 1,
            "page": 1,
            "text": "Python is widely used for machine learning."
        },
        {
            "chunk_id": 2,
            "page": 1,
            "text": "Football is a popular sport played around the world."
        }
    ]

    texts = [
        chunk["text"]
        for chunk in chunks
    ]

    embeddings = generate_embeddings(texts)

    vector_store.build(
        chunks,
        embeddings
    )

    query = "What is machine learning?"

    query_embedding = generate_embeddings(
        [query]
    )[0]

    results = vector_store.search(
        query_embedding,
        top_k=2
    )

    return {
        "query": query,
        "results": results
    }

@app.get("/test-document-retrieval")
def test_document_retrieval():

    chunks = [
        {
            "document_id": "doc1",
            "chunk_id": 0,
            "page": 1,
            "text": "Machine learning is a branch of artificial intelligence."
        },
        {
            "document_id": "doc1",
            "chunk_id": 1,
            "page": 1,
            "text": "Machine learning models learn patterns from data."
        },
        {
            "document_id": "doc2",
            "chunk_id": 0,
            "page": 1,
            "text": "Football is a popular sport played worldwide."
        }
    ]

    texts = [
        chunk["text"]
        for chunk in chunks
    ]

    embeddings = generate_embeddings(texts)

    vector_store.build(
        chunks,
        embeddings
    )

    query = "What is machine learning?"

    query_embedding = generate_embeddings(
        [query]
    )[0]

    results = vector_store.search(
        query_embedding=query_embedding,
        top_k=3,
        document_id="doc1"
    )

    return {
        "query": query,
        "document_id": "doc1",
        "results": results
    }

@app.get("/test-query-rewriting")
def test_query_rewriting():
    original_question="explain  machine learning?"
    rewritten_question=rewrite_query(
        original_question
    )
    return{
        "original_question":original_question,
        "rewritten_question":rewritten_question
    }


@app.get("/test-reranking")
def test_reranking():

    query = "machine learning"

    results = [
        {
            "chunk_id": 0,
            "page": 1,
            "text": "Machine learning is a branch of artificial intelligence.",
            "score": 0.75
        },
        {
            "chunk_id": 1,
            "page": 1,
            "text": "Football is a popular sport played worldwide.",
            "score": 0.70
        },
        {
            "chunk_id": 2,
            "page": 2,
            "text": "Machine learning models learn patterns from data.",
            "score": 0.72
        }
    ]

    reranked_results = rerank(
        query=query,
        results=results,
        top_k=2
    )

    return {
        "query": query,
        "results": reranked_results
    }


@app.get("/test-llm")
def test_llm():

    question = "What is machine learning?"

    context = [
        {
            "chunk_id": 0,
            "page": 1,
            "text": (
                "Machine learning is a branch of artificial "
                "intelligence that allows computers to learn "
                "patterns from data."
            )
        },
        {
            "chunk_id": 1,
            "page": 1,
            "text": (
                "Supervised learning uses labeled data to "
                "train machine learning models."
            )
        }
    ]

    answer = generate_grounded_answer(
        question=question,
        context=context
    )

    return {
        "question": question,
        "answer": answer,
        "sources": context
    }


@app.get("/test-groundedness")
def test_groundedness():

    answer = (
        "Machine learning is a branch of artificial "
        "intelligence that learns patterns from data."
    )

    context = [
        {
            "document_id": "doc1",
            "filename": "machine_learning.txt",
            "page": 1,
            "chunk_id": 0,
            "text": (
                "Machine learning is a branch of artificial "
                "intelligence that allows computers to learn "
                "patterns from data."
            ),
            "score": 0.91
        }
    ]

    grounded_result = check_groundedness(
        answer=answer,
        context=context
    )

    citations = build_citations(context)

    return {
        "answer": answer,
        "groundedness": grounded_result,
        "citations": citations
    }


@app.get("/test-workflow")
def test_workflow():
    result=rag_workflow.invoke({
        "question":"what is machine learning?"
    })
    return result

@app.get("/test-full-rag")
def test_full_rag():

    chunks = [
        {
            "document_id": "doc1",
            "filename": "machine_learning.txt",
            "page": 1,
            "chunk_id": 0,
            "text": (
                "Machine learning is a branch of artificial "
                "intelligence that allows computers to learn "
                "patterns from data."
            )
        },
        {
            "document_id": "doc1",
            "filename": "machine_learning.txt",
            "page": 2,
            "chunk_id": 1,
            "text": (
                "Supervised learning uses labeled data to train "
                "machine learning models."
            )
        }
    ]

    texts = [
        chunk["text"]
        for chunk in chunks
    ]

    embeddings = generate_embeddings(
        texts
    )

    vector_store = FAISSStore()

    vector_store.build(
        chunks,
        embeddings
    )

    # Connect FAISS with LangGraph
    set_vector_store(vector_store)

    result = rag_workflow.invoke({
        "question": "What is machine learning?"
    })

    return result