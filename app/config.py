import os 
import certifi 
from dotenv import load_dotenv

# --- AUTOMATIC SSL FIX FOR CONDA/PYTHON ENVIRONMENTS ---
ssl_cert = os.environ.get('SSL_CERT_FILE')
if ssl_cert and not os.path.exists(ssl_cert):
    os.environ['SSL_CERT_FILE'] = certifi.where()
elif not ssl_cert:
    os.environ['SSL_CERT_FILE'] = certifi.where()
# --------------------------------------------------------

load_dotenv()
from pydantic import AliasChoices, Field
from pydantic_settings import BaseSettings, SettingsConfigDict



class Settings(BaseSettings):
    # Accept the names commonly used for OpenRouter as well as the legacy
    # project name and OpenAI-compatible name.
    openai_router_api_key: str = Field(
        default='',
        validation_alias=AliasChoices(
            'OPENROUTER_API_KEY',
            'OPENAI_ROUTER_API_KEY',
            'OPENAI_API_KEY',
        ),
    )
    pinecone_api_key: str = ''
    tavily_api_key: str = ''
    pinecone_index: str = 'medical-chatbot'
    openai_router_chat_model: str = 'openai/gpt-4.1-mini'
    openai_router_embed_model: str = 'openai/text-embedding-3-small'
    openai_router_vision_model: str = 'openai/gpt-4o-mini'
    openai_router_max_tokens: int = 2048
    api_token: str = ''
    allowed_origins: str = 'http://localhost:8000,http://127.0.0.1:8000'
    model_config = SettingsConfigDict(env_file='.env', extra='ignore')



settings = Settings()
