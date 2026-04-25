"""Маршруты для CRUD-операций с заметками."""

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import PlainTextResponse, JSONResponse
from sqlalchemy.orm import Session
from typing import List, Optional

from database import get_db
from auth.models import User
from notes.schemas import NoteCreate, NoteUpdate, NoteResponse
from notes.repository import NoteRepository
from interfaces import INoteReader, INoteWriter

router = APIRouter()


def _get_reader(db: Session) -> INoteReader:
    """Возвращает интерфейс чтения заметок."""
    return NoteRepository(db)


def _get_writer(db: Session) -> INoteWriter:
    """Возвращает интерфейс записи заметок."""
    return NoteRepository(db)


def get_current_user(db: Session = Depends(get_db)) -> User:
    """Временная заглушка для пользователя."""
    raise NotImplementedError("Use dependencies.get_current_user in production")


@router.get("/", response_model=List[NoteResponse])
def list_notes(
    q: Optional[str] = None,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    reader: INoteReader = _get_reader(db)
    return reader.get_all(user.id, q)


@router.post("/", response_model=NoteResponse)
def create_note(
    data: NoteCreate,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    writer: INoteWriter = _get_writer(db)
    return writer.create(user.id, data.title, data.text or "")


@router.put("/{note_id}", response_model=NoteResponse)
def update_note(
    note_id: int,
    data: NoteUpdate,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    reader: INoteReader = _get_reader(db)
    note = reader.get_by_id(note_id, user.id)
    if not note:
        raise HTTPException(404, "Note not found")
    writer: INoteWriter = _get_writer(db)
    return writer.update(note, data.title, data.text)


@router.delete("/{note_id}")
def delete_note(
    note_id: int,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    reader: INoteReader = _get_reader(db)
    note = reader.get_by_id(note_id, user.id)
    if not note:
        raise HTTPException(404, "Note not found")
    writer: INoteWriter = _get_writer(db)
    writer.delete(note)
    return {"message": "Deleted"}


@router.get("/{note_id}/export")
def export_note(
    note_id: int,
    fmt: str = "txt",
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Экспортирует заметку в `txt` или `json`."""
    reader: INoteReader = _get_reader(db)
    note = reader.get_by_id(note_id, user.id)
    if not note:
        raise HTTPException(404, "Note not found")
    if fmt == "json":
        payload = {"id": note.id, "title": note.title, "text": note.text}
        return JSONResponse(content=payload)
    return PlainTextResponse(f"{note.title}\n\n{note.text}")
