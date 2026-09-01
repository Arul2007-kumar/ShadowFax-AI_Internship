import os

from dotenv import load_dotenv
from google import genai


load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY is not configured")


client = genai.Client(api_key=api_key)

LLM_MODEL =os.getenv("MODEL_NAME")


def generate_grounded_answer(
    question: str,
    context: list[dict]
) -> str:

    if not question.strip():
        raise ValueError("Question cannot be empty")

    if not context:
        return "I could not find relevant information in the provided document."

    context_text = "\n\n".join(
        [
            f"[Source {i + 1}]\n{item['text']}"
            for i, item in enumerate(context)
        ]
    )

    prompt = f"""
You are a document-grounded AI assistant.

Answer the user's question using ONLY the provided context.

Rules:
1. Do not use outside knowledge.
2. Do not invent information.
3. If the answer is not present in the context, say:
   "The answer is not available in the provided document."
4. Keep the answer clear and concise.
5. Mention the relevant source number when useful.

CONTEXT:
{context_text}

USER QUESTION:
{question}

ANSWER:
"""

    response = client.models.generate_content(
        model=LLM_MODEL,
        contents=prompt
    )

    return response.text.strip()