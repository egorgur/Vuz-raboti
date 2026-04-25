"""Интерфейс операций записи заметок."""

from abc import ABC, abstractmethod
from typing import Optional


class INoteWriter(ABC):
    """Контракт для записи заметок."""

    @abstractmethod
    def create(self, owner_id: int, title: str, text: str) -> object: ...

    @abstractmethod
    def update(
        self, note: object, title: Optional[str], text: Optional[str]
    ) -> object: ...

    @abstractmethod
    def delete(self, note: object) -> None: ...
