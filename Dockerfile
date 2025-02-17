# Dockerfile
FROM python:3.13-slim

WORKDIR /app

COPY . .

RUN pip install uv \
    && uv venv .venv \
    && /bin/bash -c "source .venv/bin/activate && uv pip install ."

CMD ["/app/.venv/bin/python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
