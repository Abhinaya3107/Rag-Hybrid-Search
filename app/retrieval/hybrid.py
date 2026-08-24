from app.retrieval.vector_store import VectorStore
from app.retrieval.bm25_store import BM25Store
from app.config import settings

def normalize(results: list[dict]) -> list[dict]:
    """Min-max normalize scores to 0-1 so dense and BM25 scores are comparable."""
    if not results:
        return results
    scores = [r["score"] for r in results]
    lo, hi = min(scores), max(scores)
    span = hi - lo or 1
    for r in results:
        r["score"] = (r["score"] - lo) / span
    return results

def hybrid_search(query: str, vector_store: VectorStore, bm25_store: BM25Store,
                   alpha: float = 0.5) -> list[dict]:
    """
    alpha controls the blend: 1.0 = pure dense, 0.0 = pure BM25.
    0.5 is a reasonable starting point; tune per use case.
    """
    dense_results = normalize(vector_store.search(query, settings.top_k_dense))
    bm25_results = normalize(bm25_store.search(query, settings.top_k_bm25))

    combined: dict[str, dict] = {}
    for r in dense_results:
        combined[r["id"]] = {**r, "score": alpha * r["score"]}
    for r in bm25_results:
        if r["id"] in combined:
            combined[r["id"]]["score"] += (1 - alpha) * r["score"]
        else:
            combined[r["id"]] = {**r, "score": (1 - alpha) * r["score"]}

    return sorted(combined.values(), key=lambda x: x["score"], reverse=True)