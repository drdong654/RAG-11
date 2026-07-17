# NOTE: this project also ships pyproject.toml + uv.lock. Recommend switching
# this Dockerfile to `uv sync --frozen` for reproducible, hash-locked installs
# instead of maintaining requirements.txt pins by hand.
FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

COPY . .

RUN useradd --create-home --shell /bin/bash appuser \
    && chown -R appuser:appuser /app
USER appuser

CMD ["python", "main.py"]
