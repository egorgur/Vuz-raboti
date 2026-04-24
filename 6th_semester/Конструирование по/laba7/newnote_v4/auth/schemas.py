"""
Принцип единственной ответственности (SRP).
Принцип общего замыкания (CCP): схемы аутентификации изменяются
вместе с роутером auth/ → они в одном пакете.
"""

from pydantic import BaseModel, EmailStr


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
