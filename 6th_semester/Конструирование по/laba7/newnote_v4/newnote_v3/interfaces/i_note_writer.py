"""
Принцип разделения интерфейсов (ISP).

INoteWriter описывает только операции изменения состояния заметок.
Клиенты, которым нужно только записывать данные, не обязаны
зависеть от методов чтения (INoteReader).
"""

from abc import ABC, abstractmethod
from typing import Optional


class INoteWriter(ABC):
    """Контракт только на запись заметок (ISP)."""

    @abstractmethod
    def create(self, owner_id: int, title: str, text: str) -> object: ...

    @abstractmethod
    def update(self, note: object, title: Optional[str], text: Optional[str]) -> object: ...

    @abstractmethod
    def delete(self, note: object) -> None: ...
