"""Pydantic-схемы заметок."""

from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class NoteCreate(BaseModel):
    title: str
    text:  Optional[str] = ""


class NoteUpdate(BaseModel):
    title: Optional[str] = None
    text:  Optional[str] = None


class NoteResponse(BaseModel):
    id:         int
    title:      str
    text:       str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
