"""
Принцип единственной ответственности (SRP).

PasswordService отвечает только за хэширование паролей
и их верификацию через bcrypt. Единственная причина для изменения
этого модуля — смена алгоритма хэширования.

До рефакторинга: весь auth_utils.py нарушал SRP, объединяя
в одном файле три несвязанные обязанности:
    1. хэширование паролей (теперь → password_service.py),
    2. работу с JWT-токенами (теперь → token_service.py),
    3. генерацию OTP-кодов (теперь → otp_service.py).
"""

from passlib.context import CryptContext

_pwd_context = CryptContext(schemes=["bcrypt"])


class PasswordService:
    """Отвечает исключительно за безопасное хранение паролей."""

    @staticmethod
    def hash(password: str) -> str:
        return _pwd_context.hash(password)

    @staticmethod
    def verify(password: str, hashed: str) -> bool:
        return _pwd_context.verify(password, hashed)
