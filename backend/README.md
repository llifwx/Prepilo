# Prepilo Backend

FastAPI backend for Prepilo MVP V1.

## What Is Implemented

- `GET /health`
- `POST /api/auth/register`
- `POST /api/auth/login`
- `GET /api/users/me`
- `PATCH /api/users/me`
- CRUD for `/api/subjects`
- CRUD for `/api/topics` with ownership checks through the parent subject

## Stack

- Python 3.12+
- FastAPI
- SQLAlchemy
- Pydantic Settings
- JWT auth with `python-jose`
- Password hashing with `passlib` and `bcrypt`
- Ruff for backend linting

## Setup

Run all backend commands from `backend/`.

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
```

Create `.env` if you need values different from local defaults:

```env
APP_ENV=local
DATABASE_URL=sqlite:///./prepilo.db
SECRET_KEY=change-me-locally
ACCESS_TOKEN_EXPIRE_MINUTES=1440
JWT_ALGORITHM=HS256
```

## Database

The current MVP backend does not have Alembic migrations yet. For local SQLite development, create tables from SQLAlchemy models:

```bash
python -c "from app.core.database import Base, engine; import app.modules.users.models, app.modules.subjects.models, app.modules.topics.models; Base.metadata.create_all(bind=engine)"
```

This creates `backend/prepilo.db` when `DATABASE_URL=sqlite:///./prepilo.db`.

## Run

```bash
uvicorn app.main:app --reload
```

Backend will be available at:

- API: `http://127.0.0.1:8000`
- Swagger: `http://127.0.0.1:8000/docs`
- Health check: `http://127.0.0.1:8000/health`

## Quality Checks

```bash
ruff check .
pytest
```

`pytest` is prepared as a dev dependency, but the repository does not contain backend tests yet.
