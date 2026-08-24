from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    anthropic_api_key: str
    embedding_model: str = "all-MiniLM-L6-v2"
    reranker_model: str = "cross-encoder/ms-marco-MiniLM-L-6-v2"
    llm_model: str = "claude-sonnet-4-5"
    chunk_size: int = 500
    chunk_overlap: int = 50
    top_k_dense: int = 10
    top_k_bm25: int = 10
    top_k_final: int = 5
    chroma_path: str = "storage/chroma"
    bm25_path: str = "storage/bm25_index.pkl"

    class Config:
        env_file = ".env"

settings = Settings()