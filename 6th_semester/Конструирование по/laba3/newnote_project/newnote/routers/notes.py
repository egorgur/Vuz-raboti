from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from database import get_db
from models import Note, User
from schemas import NoteCreate, NoteUpdate, NoteResponse
from dependencies import get_current_user

router = APIRouter()


@router.get("/", response_model=List[NoteResponse])
def list_notes(
    q:    Optional[str] = None,
    user: User           = Depends(get_current_user),
    db:   Session        = Depends(get_db),
):
    """Return all notes for the current user; filter by title keyword if q is set."""
    query = db.query(Note).filter(Note.owner_id == user.id)
    if q:
        query = query.filter(Note.title.ilike(f"%{q}%"))
    return query.order_by(Note.updated_at.desc()).all()


@router.post("/", response_model=NoteResponse)
def create_note(
    data: NoteCreate,
    user: User    = Depends(get_current_user),
    db:   Session = Depends(get_db),
):
    note = Note(**data.model_dump(), owner_id=user.id)
    db.add(note)
    db.commit()
    db.refresh(note)
    return note


@router.put("/{note_id}", response_model=NoteResponse)
def update_note(
    note_id: int,
    data:    NoteUpdate,
    user:    User    = Depends(get_current_user),
    db:      Session = Depends(get_db),
):
    note = db.query(Note).filter(Note.id == note_id, Note.owner_id == user.id).first()
    if not note:
        raise HTTPException(404, "Note not found")
    for field, value in data.model_dump(exclude_none=True).items():
        setattr(note, field, value)
    note.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(note)
    return note


@router.delete("/{note_id}")
def delete_note(
    note_id: int,
    user:    User    = Depends(get_current_user),
    db:      Session = Depends(get_db),
):
    note = db.query(Note).filter(Note.id == note_id, Note.owner_id == user.id).first()
    if not note:
        raise HTTPException(404, "Note not found")
    db.delete(note)
    db.commit()
    return {"message": "Deleted"}
