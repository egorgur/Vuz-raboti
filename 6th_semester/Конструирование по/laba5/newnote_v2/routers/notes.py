from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import PlainTextResponse, JSONResponse
from sqlalchemy.orm import Session
from typing import List, Optional

from database import get_db
from models import User
from schemas import NoteCreate, NoteUpdate, NoteResponse
from dependencies import get_current_user
from patterns.note_repository import NoteRepository
from patterns.note_exporter import get_exporter_factory

router = APIRouter()


def _repo(db: Session) -> NoteRepository:
    return NoteRepository(db)


@router.get("/", response_model=List[NoteResponse])
def list_notes(
    q: Optional[str] = None,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return _repo(db).get_all(user.id, q)


@router.post("/", response_model=NoteResponse)
def create_note(
    data: NoteCreate,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return _repo(db).create(user.id, data.title, data.text or "")


@router.put("/{note_id}", response_model=NoteResponse)
def update_note(
    note_id: int,
    data: NoteUpdate,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    repo = _repo(db)
    note = repo.get_by_id(note_id, user.id)
    if not note:
        raise HTTPException(404, "Note not found")
    return repo.update(note, data.title, data.text)


@router.delete("/{note_id}")
def delete_note(
    note_id: int,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    repo = _repo(db)
    note = repo.get_by_id(note_id, user.id)
    if not note:
        raise HTTPException(404, "Note not found")
    repo.delete(note)
    return {"message": "Deleted"}


@router.get("/{note_id}/export")
def export_note(
    note_id: int,
    fmt: str = "txt",
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Экспортирует заметку в `txt` или `json`."""
    note = _repo(db).get_by_id(note_id, user.id)
    if not note:
        raise HTTPException(404, "Note not found")
    try:
        factory = get_exporter_factory(fmt)
    except ValueError as e:
        raise HTTPException(400, str(e))
    content, content_type = factory.get_export(note)
    if fmt == "json":
        return JSONResponse(content=content, media_type=content_type)
    return PlainTextResponse(content=content, media_type=content_type)
