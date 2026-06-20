from app.services.embedding_service import get_embedding

embedding = get_embedding("Python FastAPI PostgreSQL")

print(type(embedding))
print(len(embedding))
print(embedding[:5])