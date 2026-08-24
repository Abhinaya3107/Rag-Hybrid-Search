from sentence_transformers import CrossEncoder
from app.config import settings

_reranker = CrossEncoder(settings.reranker_model)

def rerank(query: str, candidates: list[dict], top_k: int) -> list[dict]:
    pairs = [(query, c["text"]) for c in candidates]
    scores = _reranker.predict(pairs)
    for c, s in zip(candidates, scores):
        c["rerank_score"] = float(s)
    return sorted(candidates, key=lambda x: x["rerank_score"], reverse=True)[:top_k]