"""
Принцип единственной ответственности (SRP).

TokenService отвечает только за создание и декодирование JWT-токенов.
Единственная причина для изменения — смена алгоритма подписи или
формата токена.
"""

from datetime import datetime, timedelta
from jose import jwt, JWTError

SECRET_KEY         = "change-me-in-production"
ALGORITHM          = "HS256"
TOKEN_EXPIRE_HOURS = 6


class TokenService:
    """Отвечает исключительно за JWT-токены."""

    @staticmethod
    def create(user_id: int) -> str:
        expire = datetime.utcnow() + timedelta(hours=TOKEN_EXPIRE_HOURS)
        return jwt.encode({"sub": str(user_id), "exp": expire}, SECRET_KEY, algorithm=ALGORITHM)

    @staticmethod
    def decode(token: str) -> int:
        """Декодирует токен и возвращает user_id. Бросает JWTError при невалидном токене."""
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return int(payload["sub"])
