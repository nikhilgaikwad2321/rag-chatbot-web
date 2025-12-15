from sklearn.feature_extraction.text import TfidfVectorizer

# Global vectorizer (IMPORTANT)
vectorizer = TfidfVectorizer(
    stop_words="english",
    max_features=5000
)

def generate_embeddings(texts):
    """
    Fit TF-IDF on document chunks
    """
    embeddings = vectorizer.fit_transform(texts)
    return embeddings.toarray()

def embed_query(query):
    """
    Transform query using SAME vectorizer
    """
    embedding = vectorizer.transform([query])
    return embedding.toarray()[0]
