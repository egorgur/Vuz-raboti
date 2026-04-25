"""Точка входа сервиса заметок."""

from fastapi import FastAPI
from notes_service.database import Base, engine
from notes_service.router import router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="NewNote Notes Service", version="2.0")
app.include_router(router, prefix="/notes")
