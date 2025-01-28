FROM python:3.11-slim

WORKDIR /hatico

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir poetry

COPY pyproject.toml poetry.lock /hatico/

RUN poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi --no-root

COPY alembic.ini /hatico/
COPY migrations /hatico/migrations

COPY . /hatico

ENV PYTHONPATH=/hatico
