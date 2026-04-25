"""Репозиторий заметок на SQLAlchemy."""

from datetime import datetime
from typing import List, Optional
from sqlalchemy.orm import Session

from interfaces.i_note_reader import INoteReader
from interfaces.i_note_writer import INoteWriter
from notes.models import Note


class NoteRepository(INoteReader, INoteWriter):
    """Реализация интерфейсов чтения и записи заметок."""

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
