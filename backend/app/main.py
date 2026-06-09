from fastapi import FastAPI

from app.modules.auth.router import router as auth_router
from app.modules.subjects.router import router as subjects_router
from app.modules.topics.router import router as topics_router
from app.modules.users.router import router as users_router

app = FastAPI(title="Prepilo API", version="0.1.0")


@app.get("/health", tags=["health"])
def health_check() -> dict[str, str]:
    return {"status": "ok"}


app.include_router(auth_router, prefix="/api/auth", tags=["auth"])
app.include_router(users_router, prefix="/api/users", tags=["users"])
app.include_router(subjects_router, prefix="/api/subjects", tags=["subjects"])
app.include_router(topics_router, prefix="/api/topics", tags=["topics"])
