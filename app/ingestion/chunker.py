def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> list[str]:
    """
    Splits text into overlapping word-based chunks.
    Overlap keeps context from being cut awkwardly at chunk boundaries —
    e.g. a sentence that explains a term defined just before the split.
    """
    words = text.split()
    chunks = []
    start = 0
    while start < len(words):
        end = start + chunk_size
        chunk = " ".join(words[start:end])
        if chunk.strip():
            chunks.append(chunk)
        start += chunk_size - overlap
    return chunks

def chunk_documents(docs: list[dict], chunk_size: int, overlap: int) -> list[dict]:
    """Returns [{"id": ..., "text": ..., "source": ...}, ...]"""
    all_chunks = []
    for doc in docs:
        pieces = chunk_text(doc["text"], chunk_size, overlap)
        for i, piece in enumerate(pieces):
            all_chunks.append({
                "id": f"{doc['source']}__chunk{i}",
                "text": piece,
                "source": doc["source"],
            })
    return all_chunks