"""
Notes Service — микросервис управления заметками.

Ответственность: CRUD-операции с заметками.
Идентификация пользователя — из заголовков X-User-Id и X-User-Role,
проставленных API Gateway после проверки JWT.
Имеет собственную базу данных (notes.db).
"""

from fastapi import FastAPI
from notes_service.database import Base, engine
from notes_service.router import router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="NewNote Notes Service", version="2.0")
app.include_router(router, prefix="/notes")
