from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from users.models import User
from users.dependencies import get_user_reader, get_user_writer
from notes.models import Note
from notes.schemas import NoteResponse
from security.rbac import require_role, Role
from interfaces import IUserReader, IUserWriter  # DIP: зависимость от абстракций

router = APIRouter()


@router.get("/users", response_model=List[dict])
def list_all_users(
    reader: IUserReader = Depends(get_user_reader),
    admin:  User        = Depends(require_role(Role.ADMIN)),   # ← RBAC: только admin
):
    """Просмотр всех пользователей (только для администратора)."""
    users = reader.get_all()
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
    reader:  IUserReader = Depends(get_user_reader),
    writer:  IUserWriter = Depends(get_user_writer),
    admin:   User        = Depends(require_role(Role.ADMIN)),
):
    """Удаление пользователя (только для администратора)."""
    user = reader.get_by_id(user_id)
    if not user:
        from fastapi import HTTPException
        raise HTTPException(404, "User not found")
    writer.delete(user)
    return {"message": f"User {user_id} deleted"}
