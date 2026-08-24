import chromadb
from app.config import settings
from app.retrieval.embeddings import embed_texts

class VectorStore:
    def __init__(self):
        self.client = chromadb.PersistentClient(path=settings.chroma_path)
        self.collection = self.client.get_or_create_collection("documents")

    def add_chunks(self, chunks: list[dict]):
        embeddings = embed_texts([c["text"] for c in chunks])
        self.collection.add(
            ids=[c["id"] for c in chunks],
            documents=[c["text"] for c in chunks],
            embeddings=embeddings,
            metadatas=[{"source": c["source"]} for c in chunks],
        )

    def search(self, query: str, top_k: int) -> list[dict]:
        query_embedding = embed_texts([query])[0]
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
        )
        return [
            {"id": id_, "text": doc, "source": meta["source"], "score": 1 - dist}
            for id_, doc, meta, dist in zip(
                results["ids"][0], results["documents"][0],
                results["metadatas"][0], results["distances"][0],
            )
        ]