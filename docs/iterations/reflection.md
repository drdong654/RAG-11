# FEAT: 1

**Что сделано:** настроены PostgreSQL (pgvector), SQLAlchemy-модель User, репозиторий, FastAPI-эндпоинты (/users, /users/{telegram_id}), docker compose (bot + api + db).

**План на следующую неделю:** интегрировать RAG-pайплайн в FastAPI — загрузка документов, чанкинг, векторный поиск через pgvector, эндпоинт для вопросов.