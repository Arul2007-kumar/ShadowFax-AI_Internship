from typing import TypedDict


class RAGState(TypedDict, total=False):

    question: str

    rewritten_query: str

    retrieved_chunks: list[dict]

    reranked_chunks: list[dict]

    answer: str

    grounded: bool

    confidence: float

    citations: list[dict]

    error: str