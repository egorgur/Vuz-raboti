from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from auth_service.database import get_db
from auth_service.repository import UserRepository
from auth_service.schemas import RegisterRequest, LoginRequest, SmsRequest, SmsVerifyRequest, TokenResponse
from auth_service.security import (
    hash_password, verify_password, create_token, generate_otp, rate_limit,
)
from auth_service.notification import notify

router = APIRouter()


def get_users(db: Session = Depends(get_db)) -> UserRepository:
    return UserRepository(db)


@router.post("/register", response_model=TokenResponse)
def register(data: RegisterRequest, request: Request, users: UserRepository = Depends(get_users)):
    rate_limit(request, "register")
    if users.get_by_email(data.email):
        raise HTTPException(400, "Email already registered")
    user = users.create(data.email, hash_password(data.password), data.phone)
    return {"access_token": create_token(user.id, user.role)}


@router.post("/login", response_model=TokenResponse)
def login(data: LoginRequest, request: Request, users: UserRepository = Depends(get_users)):
    rate_limit(request, "login")
    user = users.get_by_email(data.email)
    if not user or not verify_password(data.password, user.password_hash):
        raise HTTPException(401, "Invalid credentials")
    return {"access_token": create_token(user.id, user.role)}


@router.post("/sms/send")
def send_sms(data: SmsRequest, request: Request, users: UserRepository = Depends(get_users)):
    rate_limit(request, "sms")
    user = users.get_by_phone(data.phone)
    if not user:
        raise HTTPException(404, "Not registered")
    user.sms_code = generate_otp()
    user.sms_code_expires = datetime.utcnow() + timedelta(minutes=5)
    users.save(user)
    notify("sms", user.phone, f"Your code: {user.sms_code}")
    return {"message": "SMS sent"}


@router.post("/sms/verify", response_model=TokenResponse)
def verify_sms(data: SmsVerifyRequest, request: Request, users: UserRepository = Depends(get_users)):
    rate_limit(request, "sms_verify")
    user = users.get_by_phone(data.phone)
    if not user or user.sms_code != data.code:
        raise HTTPException(401, "Invalid code")
    if not user.sms_code_expires or datetime.utcnow() > user.sms_code_expires:
        raise HTTPException(401, "Code expired")
    user.sms_code = None
    users.save(user)
    return {"access_token": create_token(user.id, user.role)}
