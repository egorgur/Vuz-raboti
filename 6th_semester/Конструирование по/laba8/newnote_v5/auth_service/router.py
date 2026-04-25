from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from pydantic import BaseModel, EmailStr
from passlib.context import CryptContext
from jose import jwt
import random, time
from collections import defaultdict

from auth_service.database import get_db
from auth_service.models import User

router = APIRouter()

SECRET_KEY = "change-me-in-production"
ALGORITHM  = "HS256"
_pwd = CryptContext(schemes=["bcrypt"])
_attempts: dict = defaultdict(list)


def _rate_limit(request: Request, ep: str):
    ip  = request.client.host if request.client else "unknown"
    key = f"{ip}:{ep}"
    now = time.time()
    _attempts[key] = [t for t in _attempts[key] if t > now - 60]
    if len(_attempts[key]) >= 5:
        raise HTTPException(429, "Too many attempts")
    _attempts[key].append(now)


def _token(user_id: int, role: str) -> str:
    exp = datetime.utcnow() + timedelta(hours=6)
    return jwt.encode({"sub": str(user_id), "role": role, "exp": exp}, SECRET_KEY, algorithm=ALGORITHM)


class RegisterReq(BaseModel):
    email: EmailStr
    phone: str
    password: str

class LoginReq(BaseModel):
    email: EmailStr
    password: str

class SmsReq(BaseModel):
    phone: str

class SmsVerifyReq(BaseModel):
    phone: str
    code: str


@router.post("/register")
def register(data: RegisterReq, request: Request, db: Session = Depends(get_db)):
    _rate_limit(request, "register")
    if db.query(User).filter(User.email == data.email).first():
        raise HTTPException(400, "Email already registered")
    user = User(email=data.email, phone=data.phone, password_hash=_pwd.hash(data.password))
    db.add(user); db.commit(); db.refresh(user)
    return {"access_token": _token(user.id, user.role)}


@router.post("/login")
def login(data: LoginReq, request: Request, db: Session = Depends(get_db)):
    _rate_limit(request, "login")
    user = db.query(User).filter(User.email == data.email).first()
    if not user or not _pwd.verify(data.password, user.password_hash):
        raise HTTPException(401, "Invalid credentials")
    return {"access_token": _token(user.id, user.role)}


@router.post("/sms/send")
def send_sms(data: SmsReq, request: Request, db: Session = Depends(get_db)):
    _rate_limit(request, "sms")
    user = db.query(User).filter(User.phone == data.phone).first()
    if not user:
        raise HTTPException(404, "Not registered")
    user.sms_code = str(random.randint(100000, 999999))
    user.sms_code_expires = datetime.utcnow() + timedelta(minutes=5)
    db.commit()
    return {"message": "SMS sent"}


@router.post("/sms/verify")
def verify_sms(data: SmsVerifyReq, request: Request, db: Session = Depends(get_db)):
    _rate_limit(request, "sms_verify")
    user = db.query(User).filter(User.phone == data.phone).first()
    if not user or user.sms_code != data.code:
        raise HTTPException(401, "Invalid code")
    if not user.sms_code_expires or datetime.utcnow() > user.sms_code_expires:
        raise HTTPException(401, "Code expired")
    user.sms_code = None; db.commit()
    return {"access_token": _token(user.id, user.role)}
