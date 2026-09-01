def check_groundedness(
    answer: str,
    context: list[dict]
) -> dict:

    if not answer.strip():
        return {
            "grounded": False,
            "confidence": 0.0,
            "reason": "Empty answer"
        }

    if not context:
        return {
            "grounded": False,
            "confidence": 0.0,
            "reason": "No context available"
        }

    answer_words = set(answer.lower().split())

    context_text = " ".join(
        item.get("text", "")
        for item in context
    ).lower()

    context_words = set(context_text.split())

    if not answer_words:
        return {
            "grounded": False,
            "confidence": 0.0,
            "reason": "No meaningful answer content"
        }

    matched_words = answer_words.intersection(
        context_words
    )

    confidence = len(matched_words) / len(answer_words)

    grounded = confidence >= 0.30

    return {
        "grounded": grounded,
        "confidence": round(confidence, 2),
        "reason": (
            "Answer is supported by retrieved context"
            if grounded
            else
            "Answer has insufficient support in retrieved context"
        )
    }


def build_citations(
    context: list[dict]
) -> list[dict]:

    citations = []

    for item in context:

        citations.append({
            "document_id": item.get("document_id"),
            "filename": item.get("filename"),
            "page": item.get("page"),
            "chunk_id": item.get("chunk_id"),
            "score": item.get("rerank_score", item.get("score", 0.0))
        })

    return citations