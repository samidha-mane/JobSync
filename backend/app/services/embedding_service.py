from sentence_transformers import SentenceTransformer
import numpy as np

model = SentenceTransformer("all-MiniLM-L6-v2")

def get_embedding(text: str) -> list:
    embedding = model.encode(text, normalize_embeddings=True)
    return embedding.tolist()

def cosine_similarity(vec_a: list, vec_b: list) -> float:
    a = np.array(vec_a)
    b = np.array(vec_b)
    return float(np.dot(a, b))