from datetime import datetime
from typing import List, Optional

from sqlalchemy.orm import Session

from notes_service.models import Note


class NoteRepository:
    def __init__(self, db: Session):
        self.db = db

    def list(self, owner_id: int, q: Optional[str] = None) -> List[Note]:
        query = self.db.query(Note).filter(Note.owner_id == owner_id)
        if q:
            query = query.filter(Note.title.ilike(f"%{q}%"))
        return query.order_by(Note.updated_at.desc()).all()

    def get(self, note_id: int, owner_id: Optional[int] = None) -> Optional[Note]:
        query = self.db.query(Note).filter(Note.id == note_id)
        if owner_id is not None:
            query = query.filter(Note.owner_id == owner_id)
        return query.first()

    def create(self, owner_id: int, title: str, text: str) -> Note:
        note = Note(title=title, text=text, owner_id=owner_id)
        self.db.add(note)
        self.db.commit()
        self.db.refresh(note)
        return note

    def update(self, note: Note, title: Optional[str], text: Optional[str]) -> Note:
        if title is not None:
            note.title = title
        if text is not None:
            note.text = text
        note.updated_at = datetime.utcnow()
        self.db.commit()
        self.db.refresh(note)
        return note

    def delete(self, note: Note) -> None:
        self.db.delete(note)
        self.db.commit()
