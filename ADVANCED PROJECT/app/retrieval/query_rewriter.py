def rewrite_query(question: str) -> str:

    question = question.strip()

    if not question:
        raise ValueError("Question cannot be empty")

    # Remove unnecessary spaces
    question = " ".join(question.split())

    # Simple refinement rules
    replacements = {
        "tell me about": "",
        "explain": "",
        "what is": "",
        "what are": "",
        "can you explain": "",
    }

    refined_query = question.lower()

    for old, new in replacements.items():
        refined_query = refined_query.replace(old, new)

    refined_query = refined_query.strip()

    # If removing the question words makes it too short,
    # use the original question.
    if len(refined_query) < 3:
        return question

    return refined_query