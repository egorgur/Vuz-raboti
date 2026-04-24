"""
Паттерн проектирования: Стратегия (Strategy) — поведенческий.

Контекст: При аутентификации пользователь может выбрать один из двух способов
входа: по e-mail + пароль или по одноразовому SMS-коду. Оба способа имеют
общий интерфейс (метод authenticate), но различную реализацию.
Паттерн позволяет переключать алгоритм аутентификации без изменения кода,
который его использует.

Когда НЕ использовать Шаблонный метод (Template Method):
Шаблонный метод подходит, когда у всех вариантов есть фиксированная
последовательность шагов. Здесь же у e-mail и SMS-аутентификации нет
общих шагов — это принципиально разные алгоритмы. Поэтому выбрана Стратегия.
"""

from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from fastapi import HTTPException
from sqlalchemy.orm import Session

from models import User
import auth_utils


class AuthStrategy(ABC):
    """Абстрактная стратегия аутентификации."""

    @abstractmethod
    def authenticate(self, db: Session, **kwargs) -> str:
        """Выполняет аутентификацию и возвращает JWT-токен."""
        ...


class EmailAuthStrategy(AuthStrategy):
    """Конкретная стратегия: вход по e-mail и паролю."""

    def authenticate(self, db: Session, **kwargs) -> str:
        email = kwargs["email"]
        password = kwargs["password"]
        user: User | None = db.query(User).filter(User.email == email).first()
        if not user or not auth_utils.verify_password(password, user.password_hash):
            raise HTTPException(status_code=401, detail="Invalid credentials")
        return auth_utils.create_token(user.id)


class SmsAuthStrategy(AuthStrategy):
    """Конкретная стратегия: вход по одноразовому SMS-коду (OTP)."""

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
    """Контекст, использующий стратегию аутентификации."""

    def __init__(self, strategy: AuthStrategy) -> None:
        self._strategy = strategy

    def set_strategy(self, strategy: AuthStrategy) -> None:
        self._strategy = strategy

    def login(self, db: Session, **kwargs) -> str:
        return self._strategy.authenticate(db, **kwargs)
