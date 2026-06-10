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
- Alembic
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

For MVP V1, use a local database first. The default config uses SQLite:

```env
DATABASE_URL=sqlite:///./prepilo.db
```

Apply migrations:

```bash
alembic upgrade head
```

In `APP_ENV=local`, the app also runs `alembic upgrade head` on startup. This gives automatic local table creation while still keeping schema state inside Alembic. For staging and production, run migrations explicitly during deploy.

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
