from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


# ── Auth ──────────────────────────────────────────────────────────────────────

class RegisterRequest(BaseModel):
    email:    EmailStr
    phone:    str
    password: str

class LoginRequest(BaseModel):
    email:    EmailStr
    password: str

class SmsRequest(BaseModel):
    phone: str

class SmsVerifyRequest(BaseModel):
    phone: str
    code:  str

class TokenResponse(BaseModel):
    access_token: str
    token_type:   str = "bearer"


# ── Notes ─────────────────────────────────────────────────────────────────────

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
