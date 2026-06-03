from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional

from notes_service.database import get_db
from notes_service.repository import NoteRepository
from notes_service.schemas import NoteCreate, NoteUpdate, NoteOut
from notes_service.security import current_user, CurrentUser

router = APIRouter()


def get_notes(db: Session = Depends(get_db)) -> NoteRepository:
    return NoteRepository(db)


@router.get("/", response_model=List[NoteOut])
def list_notes(
    q: Optional[str] = None,
    owner_id: Optional[int] = None,
    user: CurrentUser = Depends(current_user),
    notes: NoteRepository = Depends(get_notes),
):
    target = owner_id if owner_id and user.is_admin else user.id
    return notes.list(target, q)


@router.post("/", response_model=NoteOut)
def create_note(
    data: NoteCreate,
    user: CurrentUser = Depends(current_user),
    notes: NoteRepository = Depends(get_notes),
):
    return notes.create(user.id, data.title, data.text or "")


@router.put("/{note_id}", response_model=NoteOut)
def update_note(
    note_id: int,
    data: NoteUpdate,
    user: CurrentUser = Depends(current_user),
    notes: NoteRepository = Depends(get_notes),
):
    note = notes.get(note_id, user.id)
    if not note:
        raise HTTPException(404, "Note not found")
    return notes.update(note, data.title, data.text)


@router.delete("/{note_id}")
def delete_note(
    note_id: int,
    user: CurrentUser = Depends(current_user),
    notes: NoteRepository = Depends(get_notes),
):
    note = notes.get(note_id, None if user.is_admin else user.id)
    if not note:
        raise HTTPException(404, "Note not found")
    notes.delete(note)
    return {"message": "Deleted"}
