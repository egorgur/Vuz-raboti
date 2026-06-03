from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class NoteCreate(BaseModel):
    title: str
    text:  Optional[str] = ""


class NoteUpdate(BaseModel):
    title: Optional[str] = None
    text:  Optional[str] = None


class NoteOut(BaseModel):
    id:         int
    title:      str
    text:       str
    created_at: datetime
    updated_at: datetime
    model_config = {"from_attributes": True}
