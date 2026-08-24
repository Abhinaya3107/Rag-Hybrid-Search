from sentence_transformers import SentenceTransformer
from app.config import settings

_model = SentenceTransformer(settings.embedding_model)

def embed_texts(texts: list[str]) -> list[list[float]]:
    return _model.encode(texts, show_progress_bar=False).tolist()