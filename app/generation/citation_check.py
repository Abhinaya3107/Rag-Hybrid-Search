import re

def extract_cited_sources(answer: str) -> set[str]:
    return set(re.findall(r"\[([^\]]+)\]", answer))

def verify_citations(answer: str, retrieved_chunks: list[dict]) -> dict:
    """
    Flags citations the model invented that weren't actually in the
    retrieved context — this is the check that catches hallucinated sources.
    """
    cited = extract_cited_sources(answer)
    valid_sources = {c["source"] for c in retrieved_chunks}
    unverified = cited - valid_sources
    return {
        "cited_sources": list(cited),
        "unverified_citations": list(unverified),
        "fully_grounded": len(unverified) == 0,
    }