FROM python:3.13-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY . .

RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir .

RUN useradd --create-home --shell /bin/bash appuser \
    && chown -R appuser:appuser /app

USER appuser

CMD ["python", "-m", "bot.main"]