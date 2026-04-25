"""Маршруты аутентификации."""

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from database import get_db
from auth.models import User
from auth.schemas import (
    RegisterRequest,
    LoginRequest,
    SmsRequest,
    SmsVerifyRequest,
    TokenResponse,
)
from auth.password_service import PasswordService
from auth.token_service import TokenService
from auth.otp_service import OtpService
from auth.strategies import AuthContext, EmailAuthStrategy, SmsAuthStrategy
from security.rate_limiter import check_rate_limit

router = APIRouter()


@router.post("/register", response_model=TokenResponse)
def register(data: RegisterRequest, request: Request, db: Session = Depends(get_db)):
    check_rate_limit(request, "register")
    if db.query(User).filter(User.email == data.email).first():
        raise HTTPException(400, "Email already registered")
    user = User(
        email=data.email,
        phone=data.phone,
        password_hash=PasswordService.hash(data.password),
        role="user",
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"access_token": TokenService.create(user.id)}


@router.post("/login", response_model=TokenResponse)
def login(data: LoginRequest, request: Request, db: Session = Depends(get_db)):
    check_rate_limit(request, "login")
    token = AuthContext(EmailAuthStrategy()).login(
        db, email=data.email, password=data.password
    )
    return {"access_token": token}


@router.post("/sms/send")
def send_sms(data: SmsRequest, request: Request, db: Session = Depends(get_db)):
    check_rate_limit(request, "sms_send")
    user = db.query(User).filter(User.phone == data.phone).first()
    if not user:
        raise HTTPException(404, "Phone not registered")
    user.sms_code = OtpService.generate()
    user.sms_code_expires = datetime.utcnow() + timedelta(minutes=5)
    db.commit()
    return {"message": "SMS sent"}


@router.post("/sms/verify", response_model=TokenResponse)
def verify_sms(data: SmsVerifyRequest, request: Request, db: Session = Depends(get_db)):
    check_rate_limit(request, "sms_verify")
    token = AuthContext(SmsAuthStrategy()).login(db, phone=data.phone, code=data.code)
    return {"access_token": token}
