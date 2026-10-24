from functools import lru_cache
from pinecone import Pinecone, ServerlessSpec
from openai import OpenAI
from app.config import settings

@lru_cache()
def clients():
    if not settings.openai_router_api_key:
        raise ValueError(
            "Set OPENROUTER_API_KEY in your .env file to your OpenRouter key."
        )
    if not settings.pinecone_api_key:
        raise ValueError("Set PINECONE_API_KEY in your .env file.")
    # OpenRouter implements the OpenAI client API, but requires its own base URL.
    return (
        OpenAI(
            api_key=settings.openai_router_api_key,
            base_url='https://openrouter.ai/api/v1',
        ),
        Pinecone(api_key=settings.pinecone_api_key),
    )


def ensure_index():
    _, pc = clients()
    if not pc.has_index(settings.pinecone_index):
        pc.create_index(name=settings.pinecone_index, dimension=1536, metric='cosine', spec=ServerlessSpec(cloud='aws', region='us-east-1'))
    return pc.Index(settings.pinecone_index)


def embed(texts):
    ai, _ = clients()
    model = settings.openai_router_embed_model
    # Keep older .env model IDs working with OpenRouter's provider/model IDs.
    if '/' not in model:
        model = f'openai/{model}'
    return [x.embedding for x in ai.embeddings.create(model=model, input=texts).data]



def search_kb(query, top_k=5):
    index = ensure_index()
    vector = embed([query])[0]
    result = index.query(vector=vector, top_k=top_k, include_metadata=True)
    return [{'page': m.metadata.get('page'), 'text': m.metadata.get('text',''), 'score': round(m.score,3), 'source': 'Gale Encyclopedia (2002)'} for m in result.matches if m.score >= 0.30]
