from pydantic import BaseModel


class QueryRequest(BaseModel):
    question: str
    top_k: int = 5


class QueryResponse(BaseModel):
    answer: str
    sources: list[str]
    fully_grounded: bool


class IngestResponse(BaseModel):
    documents_ingested: int
