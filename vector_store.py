import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

class VectorStore:
    def __init__(self, dim):
        self.embeddings = []
        self.metadata = []

    def add(self, embeddings, metadata):
        self.embeddings = embeddings
        self.metadata = metadata

    def search(self, query_embedding, k=5):
        if len(self.embeddings) == 0:
            return []

        similarities = cosine_similarity(
            [query_embedding],
            self.embeddings
        )[0]

        top_k_idx = similarities.argsort()[-k:][::-1]

        results = []
        for idx in top_k_idx:
            chunk = self.metadata[idx]
            chunk["score"] = float(similarities[idx])
            results.append(chunk)

        return results
