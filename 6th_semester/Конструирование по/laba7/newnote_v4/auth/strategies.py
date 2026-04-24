"""
Принцип открытости/закрытости (OCP): для добавления нового
способа аутентификации достаточно создать новый подкласс AuthStrategy
без изменения существующего кода.

Принцип подстановки Барбары Лисков (LSP): EmailAuthStrategy и
SmsAuthStrategy полностью взаимозаменяемы там, где ожидается
AuthStrategy — они не изменяют контракт базового класса.

Принцип общего замыкания (CCP): стратегии аутентификации изменяются
вместе с auth-роутером → они в одном пакете auth/.
"""

from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from fastapi import HTTPException
from sqlalchemy.orm import Session

from auth.models import User
from auth.password_service import PasswordService
from auth.token_service import TokenService
from auth.otp_service import OtpService


class AuthStrategy(ABC):
    """Абстрактная стратегия аутентификации (OCP + LSP)."""

    @abstractmethod
    def authenticate(self, db: Session, **kwargs) -> str: ...


class EmailAuthStrategy(AuthStrategy):
    """Аутентификация по e-mail и паролю."""

    def authenticate(self, db: Session, **kwargs) -> str:
        user: User | None = db.query(User).filter(User.email == kwargs["email"]).first()
        if not user or not PasswordService.verify(kwargs["password"], user.password_hash):
            raise HTTPException(401, "Invalid credentials")
        return TokenService.create(user.id)


class SmsAuthStrategy(AuthStrategy):
    """Аутентификация по одноразовому SMS-коду."""

    def authenticate(self, db: Session, **kwargs) -> str:
        user: User | None = db.query(User).filter(User.phone == kwargs["phone"]).first()
        if not user or user.sms_code != kwargs["code"]:
            raise HTTPException(401, "Invalid code")
        if not user.sms_code_expires or datetime.utcnow() > user.sms_code_expires:
            raise HTTPException(401, "Code expired")
        user.sms_code = None
        db.commit()
        return TokenService.create(user.id)


class AuthContext:
    def __init__(self, strategy: AuthStrategy) -> None:
        self._strategy = strategy

    def login(self, db: Session, **kwargs) -> str:
        return self._strategy.authenticate(db, **kwargs)
