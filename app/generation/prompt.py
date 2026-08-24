RAG_PROMPT_TEMPLATE = """Answer the question using only the provided context. Cite the source of each fact using the format [source_filename].

Context:
{context}

Question: {question}
"""


def build_prompt(question: str, chunks: list[dict]) -> str:
    context = "\n\n".join(f"[{c['source']}]\n{c['text']}" for c in chunks)
    return RAG_PROMPT_TEMPLATE.format(context=context, question=question)
