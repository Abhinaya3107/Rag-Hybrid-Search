from anthropic import Anthropic
from app.config import settings

client = Anthropic(api_key=settings.anthropic_api_key)

def generate_answer(prompt: str) -> str:
    response = client.messages.create(
        model=settings.llm_model,
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.content[0].text