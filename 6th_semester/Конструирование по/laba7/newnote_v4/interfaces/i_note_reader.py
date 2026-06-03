"""
Принцип разделения интерфейсов (ISP) и Инверсия зависимостей (DIP).

Интерфейс INoteReader описывает только операции чтения заметок.
Клиенты, которым нужно только читать (например, list_notes, get_note),
не обязаны зависеть от методов записи.

Принцип стабильных зависимостей (SDP): этот модуль стабилен — он
почти никогда не изменяется. Volatile-компоненты (notes.router) зависят
именно от этого стабильного контракта.

Принцип стабильных абстракций (SAP): пакет interfaces/ состоит
исключительно из абстракций, что делает его максимально стабильным.
"""

from abc import ABC, abstractmethod
from typing import List, Optional


class INoteReader(ABC):
    """Контракт только на чтение заметок (ISP)."""

    @abstractmethod
    def get_all(self, owner_id: int, q: Optional[str] = None) -> List: ...

    @abstractmethod
    def get_by_id(self, note_id: int, owner_id: int) -> Optional[object]: ...
