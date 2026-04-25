from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

from notes_service.database import get_db
from notes_service.models import Note

router = APIRouter()


def current_user(
    x_user_id:   str = Header(...),
    x_user_role: str = Header(default="user"),
) -> dict:
    return {"id": int(x_user_id), "role": x_user_role}


class NoteCreate(BaseModel):
    title: str
    text:  Optional[str] = ""

class NoteUpdate(BaseModel):
    title: Optional[str] = None
    text:  Optional[str] = None

class NoteOut(BaseModel):
    id: int; title: str; text: str
    created_at: datetime; updated_at: datetime
    model_config = {"from_attributes": True}


@router.get("/", response_model=List[NoteOut])
def list_notes(
    q: Optional[str] = None,
    owner_id: Optional[int] = None,
    user: dict = Depends(current_user),
    db: Session = Depends(get_db),
):
    target = user["id"]
    if owner_id and user["role"] == "admin":
        target = owner_id
    q_obj = db.query(Note).filter(Note.owner_id == target)
    if q:
        q_obj = q_obj.filter(Note.title.ilike(f"%{q}%"))
    return q_obj.order_by(Note.updated_at.desc()).all()


@router.post("/", response_model=NoteOut)
def create_note(data: NoteCreate, user: dict = Depends(current_user), db: Session = Depends(get_db)):
    note = Note(title=data.title, text=data.text or "", owner_id=user["id"])
    db.add(note); db.commit(); db.refresh(note)
    return note


@router.put("/{note_id}", response_model=NoteOut)
def update_note(note_id: int, data: NoteUpdate, user: dict = Depends(current_user), db: Session = Depends(get_db)):
    note = db.query(Note).filter(Note.id == note_id, Note.owner_id == user["id"]).first()
    if not note:
        raise HTTPException(404, "Note not found")
    if data.title is not None: note.title = data.title
    if data.text  is not None: note.text  = data.text
    note.updated_at = datetime.utcnow()
    db.commit(); db.refresh(note)
    return note


@router.delete("/{note_id}")
def delete_note(note_id: int, user: dict = Depends(current_user), db: Session = Depends(get_db)):
    q = db.query(Note).filter(Note.id == note_id)
    if user["role"] != "admin":
        q = q.filter(Note.owner_id == user["id"])
    note = q.first()
    if not note:
        raise HTTPException(404, "Note not found")
    db.delete(note); db.commit()
    return {"message": "Deleted"}
