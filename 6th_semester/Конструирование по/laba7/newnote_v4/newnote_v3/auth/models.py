"""Модель пользователя для auth-модуля."""

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    phone = Column(String, unique=True, nullable=True)
    password_hash = Column(String, nullable=True)
    sms_code = Column(String, nullable=True)
    sms_code_expires = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    notes = relationship(
        "notes.models.Note", back_populates="owner", cascade="all, delete"
    )
