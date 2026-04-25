"""Административные маршруты."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from auth.models import User
from notes.models import Note
from notes.schemas import NoteResponse
from security.rbac import require_role, Role

router = APIRouter()


@router.get("/users", response_model=List[dict])
def list_all_users(
    db: Session = Depends(get_db),
    admin: User = Depends(require_role(Role.ADMIN)),
):
    """Возвращает список всех пользователей."""
    users = db.query(User).all()
    return [{"id": u.id, "email": u.email, "role": u.role} for u in users]


@router.get("/notes", response_model=List[NoteResponse])
def list_all_notes(
    db: Session = Depends(get_db),
    admin: User = Depends(require_role(Role.ADMIN)),
):
    """Возвращает список всех заметок."""
    return db.query(Note).order_by(Note.updated_at.desc()).all()


@router.delete("/users/{user_id}")
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    admin: User = Depends(require_role(Role.ADMIN)),
):
    """Удаляет пользователя по id."""
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(404, "User not found")
    db.delete(user)
    db.commit()
    return {"message": f"User {user_id} deleted"}
