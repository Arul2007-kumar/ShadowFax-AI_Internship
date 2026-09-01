import re


def tokenize(text: str) -> set[str]:
    """
    Convert text into normalized words.
    """

    words = re.findall(
        r"\b[a-zA-Z0-9]+\b",
        text.lower()
    )

    return set(words)


def calculate_keyword_score(
    query: str,
    text: str
) -> float:

    query_words = tokenize(query)
    text_words = tokenize(text)

    if not query_words:
        return 0.0

    common_words = query_words.intersection(text_words)

    return len(common_words) / len(query_words)


def rerank(
    query: str,
    results: list[dict],
    top_k: int = 3
) -> list[dict]:

    if not results:
        return []

    reranked_results = []

    for result in results:

        semantic_score = float(
            result.get("score", 0.0)
        )

        keyword_score = calculate_keyword_score(
            query,
            result["text"]
        )

        # Combine semantic + keyword relevance
        final_score = (
            0.7 * semantic_score
            +
            0.3 * keyword_score
        )

        updated_result = result.copy()

        updated_result["keyword_score"] = round(
            keyword_score,
            4
        )

        updated_result["rerank_score"] = round(
            final_score,
            4
        )

        reranked_results.append(
            updated_result
        )

    # Highest score first
    reranked_results.sort(
        key=lambda x: x["rerank_score"],
        reverse=True
    )

    return reranked_results[:top_k]
