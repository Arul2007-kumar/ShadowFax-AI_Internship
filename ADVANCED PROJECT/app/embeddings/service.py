import os

from dotenv import load_dotenv
from google import genai


load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY is not configured")


client = genai.Client(api_key=api_key)

EMBEDDING_MODEL = "gemini-embedding-2"


def generate_embedding(text: str) -> list[float]:

    if not text.strip():
        return []

    result = client.models.embed_content(
        model=EMBEDDING_MODEL,
        contents=text
    )

    return result.embeddings[0].values


def generate_embeddings(chunks: list[str]) -> list[list[float]]:

    embeddings = []

    for chunk in chunks:

        embedding = generate_embedding(chunk)

        if embedding:
            embeddings.append(embedding)

    return embeddings