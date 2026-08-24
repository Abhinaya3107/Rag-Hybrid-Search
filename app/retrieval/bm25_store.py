import pickle
from pathlib import Path
from rank_bm25 import BM25Okapi
from app.config import settings

class BM25Store:
    def __init__(self):
        self.chunks: list[dict] = []
        self.bm25: BM25Okapi | None = None
        if Path(settings.bm25_path).exists():
            self.load()

    def build(self, chunks: list[dict]):
        self.chunks = chunks
        tokenized = [c["text"].lower().split() for c in chunks]
        self.bm25 = BM25Okapi(tokenized)
        self._save()

    def search(self, query: str, top_k: int) -> list[dict]:
        if self.bm25 is None:
            return []
        tokenized_query = query.lower().split()
        scores = self.bm25.get_scores(tokenized_query)
        ranked = sorted(zip(self.chunks, scores), key=lambda x: x[1], reverse=True)
        return [
            {"id": c["id"], "text": c["text"], "source": c["source"], "score": float(s)}
            for c, s in ranked[:top_k] if s > 0
        ]

    def _save(self):
        Path(settings.bm25_path).parent.mkdir(parents=True, exist_ok=True)
        with open(settings.bm25_path, "wb") as f:
            pickle.dump((self.chunks, self.bm25), f)

    def load(self):
        with open(settings.bm25_path, "rb") as f:
            self.chunks, self.bm25 = pickle.load(f)