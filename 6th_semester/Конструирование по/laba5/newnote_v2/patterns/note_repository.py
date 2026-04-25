"""Репозиторий заметок на SQLAlchemy."""

from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Optional

from sqlalchemy.orm import Session
from models import Note


class AbstractNoteRepository(ABC):
    """Интерфейс репозитория заметок."""

    @abstractmethod
    def get_all(self, owner_id: int, q: Optional[str] = None) -> List[Note]: ...

    @abstractmethod
    def get_by_id(self, note_id: int, owner_id: int) -> Optional[Note]: ...

    @abstractmethod
    def create(self, owner_id: int, title: str, text: str) -> Note: ...

    @abstractmethod
    def update(self, note: Note, title: Optional[str], text: Optional[str]) -> Note: ...

    @abstractmethod
    def delete(self, note: Note) -> None: ...


class NoteRepository(AbstractNoteRepository):
    """Реализация репозитория в реляционной БД."""

    def __init__(self, db: Session) -> None:
        self._db = db

    def get_all(self, owner_id: int, q: Optional[str] = None) -> List[Note]:
        query = self._db.query(Note).filter(Note.owner_id == owner_id)
        if q:
            query = query.filter(Note.title.ilike(f"%{q}%"))
        return query.order_by(Note.updated_at.desc()).all()

    def get_by_id(self, note_id: int, owner_id: int) -> Optional[Note]:
        return (
            self._db.query(Note)
            .filter(Note.id == note_id, Note.owner_id == owner_id)
            .first()
        )

    def create(self, owner_id: int, title: str, text: str) -> Note:
        note = Note(title=title, text=text, owner_id=owner_id)
        self._db.add(note)
        self._db.commit()
        self._db.refresh(note)
        return note

    def update(self, note: Note, title: Optional[str], text: Optional[str]) -> Note:
        if title is not None:
            note.title = title
        if text is not None:
            note.text = text
        note.updated_at = datetime.utcnow()
        self._db.commit()
        self._db.refresh(note)
        return note

    def delete(self, note: Note) -> None:
        self._db.delete(note)
        self._db.commit()
