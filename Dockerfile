FROM python:3.13-slim-trixie

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_LINK_MODE=copy \
    UV_PYTHON_DOWNLOADS=never \
    UV_PROJECT_ENVIRONMENT=/app/.venv

COPY --from=ghcr.io/astral-sh/uv:0.13.6 /uv /uvx /bin/

RUN apt-get update \
    && apt-get -y install libpq-dev gcc \
    && uv pip install psycopg --system

RUN touch /app/README.md

COPY pyproject.toml uv.lock /_lock/
RUN --mount=type=cache,target=/root/.cache \
    cd /_lock && \
    uv sync \
    --frozen \
    --no-install-project \
    --no-dev

RUN useradd -m -r appuser && \
    mkdir /app/staticfiles && \
    chown -R appuser /app

COPY --chown=appuser:appuser . .

USER appuser

EXPOSE 8000

RUN chmod +x /app/entrypoint.prod.sh

CMD ["/app/entrypoint.prod.sh"]
