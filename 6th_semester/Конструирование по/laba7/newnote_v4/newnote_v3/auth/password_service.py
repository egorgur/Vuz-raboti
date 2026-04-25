"""Сервис для хэширования и проверки паролей."""

from passlib.context import CryptContext

_pwd_context = CryptContext(schemes=["bcrypt"])


class PasswordService:
    """Операции с паролями."""

    @staticmethod
    def hash(password: str) -> str:
        return _pwd_context.hash(password)

    @staticmethod
    def verify(password: str, hashed: str) -> bool:
        return _pwd_context.verify(password, hashed)
