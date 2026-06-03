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
from typing import cast
from fastapi import HTTPException
from sqlalchemy.orm import Session

from users.models import User
from users.repository import UserRepository
from auth.password_service import PasswordService
from auth.token_service import TokenService
from auth.otp_service import OtpService
from interfaces import IUserReader, IUserWriter  # DIP: зависимость от абстракций


class AuthStrategy(ABC):
    """Абстрактная стратегия аутентификации (OCP + LSP)."""

    @abstractmethod
    def authenticate(self, db: Session, **kwargs) -> str: ...


class EmailAuthStrategy(AuthStrategy):
    """Аутентификация по e-mail и паролю."""

    def authenticate(self, db: Session, **kwargs) -> str:
        reader: IUserReader = UserRepository(db)
        user = reader.get_by_email(kwargs["email"])
        if not user or not PasswordService.verify(kwargs["password"], user.password_hash):
            raise HTTPException(401, "Invalid credentials")
        return TokenService.create(user.id)


class SmsAuthStrategy(AuthStrategy):
    """Аутентификация по одноразовому SMS-коду."""

    def authenticate(self, db: Session, **kwargs) -> str:
        repo = UserRepository(db)
        reader: IUserReader = repo
        user = cast("User | None", reader.get_by_phone(kwargs["phone"]))
        if not user or user.sms_code != kwargs["code"]:
            raise HTTPException(401, "Invalid code")
        if not user.sms_code_expires or datetime.utcnow() > user.sms_code_expires:
            raise HTTPException(401, "Code expired")
        user.sms_code = None
        writer: IUserWriter = repo
        writer.save(user)
        return TokenService.create(user.id)


class AuthContext:
    def __init__(self, strategy: AuthStrategy) -> None:
        self._strategy = strategy

    def login(self, db: Session, **kwargs) -> str:
        return self._strategy.authenticate(db, **kwargs)
