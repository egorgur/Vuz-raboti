"""Сервис работы с JWT-токенами."""

from datetime import datetime, timedelta
from jose import jwt

SECRET_KEY = "change-me-in-production"
ALGORITHM = "HS256"
TOKEN_EXPIRE_HOURS = 6


class TokenService:
    @staticmethod
    def create(user_id: int, role: str = "user") -> str:
        expire = datetime.utcnow() + timedelta(hours=TOKEN_EXPIRE_HOURS)
        return jwt.encode(
            {"sub": str(user_id), "role": role, "exp": expire},
            SECRET_KEY,
            algorithm=ALGORITHM,
        )

    @staticmethod
    def decode(token: str) -> int:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return int(payload["sub"])

    @staticmethod
    def decode_role(token: str) -> str:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("role", "user")
