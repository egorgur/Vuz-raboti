"""
Точка входа приложения NewNote.
Зарегистрированы: SecurityHeadersMiddleware (аспект безопасности №2).
"""

from fastapi import FastAPI
from database import Base, engine
from auth.router import router as auth_router
from notes.router import router as notes_router
from security.headers_middleware import SecurityHeadersMiddleware  # безопасность №2

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="NewNote",
    description="Note-taking app — SOLID + components + security",
)

# Аспект безопасности №2: заголовки безопасности для всех ответов
app.add_middleware(SecurityHeadersMiddleware)

app.include_router(auth_router,  prefix="/auth",  tags=["auth"])
app.include_router(notes_router, prefix="/notes", tags=["notes"])
