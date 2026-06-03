from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import cast

from database import get_db
from users.models import User
from users.dependencies import get_user_reader, get_user_writer
from auth.schemas import RegisterRequest, LoginRequest, SmsRequest, SmsVerifyRequest, TokenResponse
from auth.password_service import PasswordService
from auth.token_service import TokenService
from auth.otp_service import OtpService
from auth.strategies import AuthContext, EmailAuthStrategy, SmsAuthStrategy
from interfaces import IUserReader, IUserWriter  # DIP: зависимость от абстракций

router = APIRouter()


@router.post("/register", response_model=TokenResponse)
def register(
    data: RegisterRequest,
    reader: IUserReader = Depends(get_user_reader),
    writer: IUserWriter = Depends(get_user_writer),
):
    if reader.get_by_email(data.email):
        raise HTTPException(400, "Email already registered")
    user = writer.create(
        email=data.email,
        phone=data.phone,
        password_hash=PasswordService.hash(data.password),
        role="user",
    )
    return {"access_token": TokenService.create(user.id)}


@router.post("/login", response_model=TokenResponse)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    token = AuthContext(EmailAuthStrategy()).login(db, email=data.email, password=data.password)
    return {"access_token": token}


@router.post("/sms/send")
def send_sms(
    data: SmsRequest,
    reader: IUserReader = Depends(get_user_reader),
    writer: IUserWriter = Depends(get_user_writer),
):
    user = cast("User | None", reader.get_by_phone(data.phone))
    if not user:
        raise HTTPException(404, "Phone not registered")
    user.sms_code = OtpService.generate()
    user.sms_code_expires = datetime.utcnow() + timedelta(minutes=5)
    writer.save(user)
    return {"message": "SMS sent"}


@router.post("/sms/verify", response_model=TokenResponse)
def verify_sms(data: SmsVerifyRequest, db: Session = Depends(get_db)):
    token = AuthContext(SmsAuthStrategy()).login(db, phone=data.phone, code=data.code)
    return {"access_token": token}
