"""Стратегии аутентификации по email и SMS."""

from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from fastapi import HTTPException
from sqlalchemy.orm import Session

from models import User
import auth_utils


class AuthStrategy(ABC):
    """Общий интерфейс стратегии аутентификации."""

    @abstractmethod
    def authenticate(self, db: Session, **kwargs) -> str:
        """Проверяет данные и возвращает JWT-токен."""
        ...


class EmailAuthStrategy(AuthStrategy):
    """Вход по e-mail и паролю."""

    def authenticate(self, db: Session, **kwargs) -> str:
        email = kwargs["email"]
        password = kwargs["password"]
        user: User | None = db.query(User).filter(User.email == email).first()
        if not user or not auth_utils.verify_password(password, user.password_hash):
            raise HTTPException(status_code=401, detail="Invalid credentials")
        return auth_utils.create_token(user.id)


class SmsAuthStrategy(AuthStrategy):
    """Вход по одноразовому SMS-коду."""

    def authenticate(self, db: Session, **kwargs) -> str:
        phone = kwargs["phone"]
        code = kwargs["code"]
        user: User | None = db.query(User).filter(User.phone == phone).first()
        if not user or user.sms_code != code:
            raise HTTPException(status_code=401, detail="Invalid code")
        if not user.sms_code_expires or datetime.utcnow() > user.sms_code_expires:
            raise HTTPException(status_code=401, detail="Code expired")
        user.sms_code = None
        db.commit()
        return auth_utils.create_token(user.id)


class AuthContext:
    """Контекст, который применяет выбранную стратегию."""

    def __init__(self, strategy: AuthStrategy) -> None:
        self._strategy = strategy

    def set_strategy(self, strategy: AuthStrategy) -> None:
        self._strategy = strategy

    def login(self, db: Session, **kwargs) -> str:
        return self._strategy.authenticate(db, **kwargs)
