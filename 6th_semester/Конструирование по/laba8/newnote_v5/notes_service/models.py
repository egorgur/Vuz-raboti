from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime
from notes_service.database import Base

class Note(Base):
    __tablename__ = "notes"
    id         = Column(Integer, primary_key=True, index=True)
    title      = Column(String, nullable=False)
    text       = Column(Text, default="")
    owner_id   = Column(Integer, nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
