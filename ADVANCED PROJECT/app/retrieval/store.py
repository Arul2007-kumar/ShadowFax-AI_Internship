import faiss
import numpy as np


class FAISSStore:

    def __init__(self):
        self.index = None
        self.chunks = []

    def build(
        self,
        chunks: list[dict],
        embeddings: list[list[float]]
    ):
        if not chunks:
            raise ValueError("No chunks available")

        if not embeddings:
            raise ValueError("No embeddings available")

        if len(chunks) != len(embeddings):
            raise ValueError(
                "Number of chunks and embeddings must be equal"
            )

        vectors = np.array(
            embeddings,
            dtype="float32"
        )

        faiss.normalize_L2(vectors)

        dimension = vectors.shape[1]

        self.index = faiss.IndexFlatIP(dimension)

        self.index.add(vectors)

        self.chunks = chunks

    def search(
        self,
        query_embedding: list[float],
        top_k: int = 5,
        document_id: str | None = None
    ) -> list[dict]:

        if self.index is None:
            raise ValueError(
                "FAISS index has not been built"
            )

        query_vector = np.array(
            [query_embedding],
            dtype="float32"
        )

        faiss.normalize_L2(query_vector)

        search_k = len(self.chunks)

        scores, indices = self.index.search(
            query_vector,
            search_k
        )

        results = []

        for score, index in zip(
            scores[0],
            indices[0]
        ):

            if index == -1:
                continue

            chunk = self.chunks[index]

            # Document-scoped filtering
            if document_id is not None:

                if chunk.get("document_id") != document_id:
                    continue

            result = chunk.copy()

            result["score"] = float(score)

            results.append(result)

            if len(results) >= top_k:
                break

        return results