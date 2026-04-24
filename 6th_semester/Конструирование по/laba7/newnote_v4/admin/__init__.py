"""
admin/router.py — административные эндпоинты, защищённые RBAC.

Доступ к GET /admin/users и GET /admin/notes разрешён только
пользователям с role=admin. Рядовой пользователь получит HTTP 403.
"""

from fastapi import APIRouter, Depends
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
    db:    Session = Depends(get_db),
    admin: User    = Depends(require_role(Role.ADMIN)),   # ← RBAC: только admin
):
    """Просмотр всех пользователей (только для администратора)."""
    users = db.query(User).all()
    return [{"id": u.id, "email": u.email, "role": u.role} for u in users]


@router.get("/notes", response_model=List[NoteResponse])
def list_all_notes(
    db:    Session = Depends(get_db),
    admin: User    = Depends(require_role(Role.ADMIN)),   # ← RBAC: только admin
):
    """Просмотр всех заметок всех пользователей (только для администратора)."""
    return db.query(Note).order_by(Note.updated_at.desc()).all()


@router.delete("/users/{user_id}")
def delete_user(
    user_id: int,
    db:      Session = Depends(get_db),
    admin:   User    = Depends(require_role(Role.ADMIN)),
):
    """Удаление пользователя (только для администратора)."""
    user = db.get(User, user_id)
    if not user:
        from fastapi import HTTPException
        raise HTTPException(404, "User not found")
    db.delete(user)
    db.commit()
    return {"message": f"User {user_id} deleted"}
