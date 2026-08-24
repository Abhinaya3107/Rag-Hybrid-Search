from fastapi import APIRouter
from pathlib import Path
from app.models.schemas import QueryRequest, QueryResponse
from app.ingestion.loader import load_all_documents
from app.ingestion.chunker import chunk_documents
from app.retrieval.vector_store import VectorStore
from app.retrieval.bm25_store import BM25Store
from app.retrieval.hybrid import hybrid_search
from app.retrieval.reranker import rerank
from app.generation.prompt import build_prompt
from app.generation.llm import generate_answer
from app.generation.citation_check import verify_citations
from app.config import settings

router = APIRouter()
vector_store = VectorStore()
bm25_store = BM25Store()

@router.post("/ingest")
def ingest():
    docs = load_all_documents(Path("data/raw"))
    chunks = chunk_documents(docs, settings.chunk_size, settings.chunk_overlap)
    vector_store.add_chunks(chunks)
    bm25_store.build(chunks)
    return {"status": "ok", "chunks_indexed": len(chunks)}

@router.post("/query", response_model=QueryResponse)
def query(req: QueryRequest):
    candidates = hybrid_search(req.question, vector_store, bm25_store)
    top_chunks = rerank(req.question, candidates, req.top_k)
    prompt = build_prompt(req.question, top_chunks)
    answer = generate_answer(prompt)
    verification = verify_citations(answer, top_chunks)
    return QueryResponse(
        answer=answer,
        sources=list({c["source"] for c in top_chunks}),
        fully_grounded=verification["fully_grounded"],
    )