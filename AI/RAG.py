import os

from agno.knowledge.knowledge import Knowledge
from agno.vectordb.pgvector import PGVector


# --- Настройки через переменные окружения (см. .env.example) ------------------
EMBEDDING_MODEL = os.environ.get("EMBEDDING", "ollama").lower()


