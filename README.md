# AI Data Agent - SDE Hiring Assignment

Conversational platform that accepts Excel uploads and answers natural-language questions about the data,
returning tables and charts.

## What's included
- `backend/` — FastAPI app (Python) that accepts Excel uploads, converts to SQLite, and exposes a simple NLQ endpoint.
- `frontend/` — React (Vite) app with file upload and chat UI (basic).
- `docker-compose.yml` — development docker compose.
- Instructions to push to GitHub.

## Quick start (local)
1. Backend:
    cd backend
    python -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
    uvicorn main:app --reload --port 8000

2. Frontend:
    cd frontend
    npm install
    npm run dev

## To push to GitHub
See instructions in `PUSH_TO_GITHUB.md`
