"""Сервис работы с JWT-токенами."""

from datetime import datetime, timedelta
from jose import jwt

SECRET_KEY = "change-me-in-production"
ALGORITHM = "HS256"
TOKEN_EXPIRE_HOURS = 6


class TokenService:
    """Создание и декодирование JWT."""

    @staticmethod
    def create(user_id: int) -> str:
        expire = datetime.utcnow() + timedelta(hours=TOKEN_EXPIRE_HOURS)
        return jwt.encode(
            {"sub": str(user_id), "exp": expire}, SECRET_KEY, algorithm=ALGORITHM
        )

    @staticmethod
    def decode(token: str) -> int:
        """Возвращает `user_id` из токена."""
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return int(payload["sub"])
