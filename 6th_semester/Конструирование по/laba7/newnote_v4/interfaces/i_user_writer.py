"""
Принцип разделения интерфейсов (ISP).

IUserWriter описывает только операции изменения состояния пользователей.
Клиенты, которым нужно только записывать данные (регистрация, выдача
OTP-кода, удаление администратором), не обязаны зависеть от методов
чтения (IUserReader).
"""

from abc import ABC, abstractmethod
from typing import Optional


class IUserWriter(ABC):
    """Контракт только на запись пользователей (ISP)."""

    @abstractmethod
    def create(
        self,
        email: str,
        password_hash: Optional[str] = None,
        phone: Optional[str] = None,
        role: str = "user",
    ) -> object: ...

    @abstractmethod
    def save(self, user: object) -> object: ...

    @abstractmethod
    def delete(self, user: object) -> None: ...
