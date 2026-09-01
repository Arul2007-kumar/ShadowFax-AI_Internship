from app.retrieval.query_rewriter import rewrite_query
from app.embeddings.service import generate_embeddings
from app.retrieval.reranker import rerank
from app.generation.llm import generate_grounded_answer
from app.generation.groundedness import (
    check_groundedness,
    build_citations
)


# Global vector store
vector_store = None


def set_vector_store(store):
    global vector_store
    vector_store = store


def rewrite_node(state):

    question = state["question"]

    rewritten_query = rewrite_query(question)

    return {
        "rewritten_query": rewritten_query
    }


def retrieve_node(state):

    global vector_store

    if vector_store is None:
        raise ValueError(
            "Vector store is not initialized"
        )

    query = state["rewritten_query"]

    query_embedding = generate_embeddings(
        [query]
    )[0]

    results = vector_store.search(
        query_embedding=query_embedding,
        top_k=5
    )

    return {
        "retrieved_chunks": results
    }


def rerank_node(state):

    query = state["rewritten_query"]

    chunks = state.get(
        "retrieved_chunks",
        []
    )

    reranked_chunks = rerank(
        query=query,
        results=chunks,
        top_k=3
    )

    return {
        "reranked_chunks": reranked_chunks
    }


def generate_node(state):

    question = state["question"]

    context = state.get(
        "reranked_chunks",
        []
    )

    answer = generate_grounded_answer(
        question=question,
        context=context
    )

    return {
        "answer": answer
    }


def groundedness_node(state):

    answer = state.get(
        "answer",
        ""
    )

    context = state.get(
        "reranked_chunks",
        []
    )

    result = check_groundedness(
        answer=answer,
        context=context
    )

    citations = build_citations(
        context
    )

    return {
        "grounded": result["grounded"],
        "confidence": result["confidence"],
        "citations": citations
    }