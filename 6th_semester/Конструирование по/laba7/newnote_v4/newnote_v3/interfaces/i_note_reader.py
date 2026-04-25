"""Интерфейс операций чтения заметок."""

from abc import ABC, abstractmethod
from typing import List, Optional


class INoteReader(ABC):
    """Контракт для чтения заметок."""

    @abstractmethod
    def get_all(self, owner_id: int, q: Optional[str] = None) -> List: ...

    @abstractmethod
    def get_by_id(self, note_id: int, owner_id: int) -> Optional[object]: ...
