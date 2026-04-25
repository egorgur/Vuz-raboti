from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from database import get_db
from models import User
from schemas import RegisterRequest, LoginRequest, SmsRequest, SmsVerifyRequest, TokenResponse
import auth_utils

router = APIRouter()


@router.post("/register", response_model=TokenResponse)
def register(data: RegisterRequest, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == data.email).first():
        raise HTTPException(400, "Email already registered")
    user = User(
        email=data.email,
        phone=data.phone,
        password_hash=auth_utils.hash_password(data.password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"access_token": auth_utils.create_token(user.id)}


@router.post("/login", response_model=TokenResponse)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email).first()
    if not user or not auth_utils.verify_password(data.password, user.password_hash):
        raise HTTPException(401, "Invalid credentials")
    return {"access_token": auth_utils.create_token(user.id)}


@router.post("/sms/send")
def send_sms(data: SmsRequest, db: Session = Depends(get_db)):
    """Генерирует и сохраняет одноразовый код для входа по SMS."""
    user = db.query(User).filter(User.phone == data.phone).first()
    if not user:
        raise HTTPException(404, "Phone not registered")
    user.sms_code = auth_utils.generate_sms_code()
    user.sms_code_expires = datetime.utcnow() + timedelta(minutes=5)
    db.commit()
    # Реальную отправку SMS подключим позже.
    return {"message": "SMS sent"}


@router.post("/sms/verify", response_model=TokenResponse)
def verify_sms(data: SmsVerifyRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.phone == data.phone).first()
    if not user or user.sms_code != data.code:
        raise HTTPException(401, "Invalid code")
    if not user.sms_code_expires or datetime.utcnow() > user.sms_code_expires:
        raise HTTPException(401, "Code expired")
    user.sms_code = None
    db.commit()
    return {"access_token": auth_utils.create_token(user.id)}
