"""
Принцип разделения интерфейсов (ISP) и Инверсия зависимостей (DIP).

Интерфейс IUserReader описывает только операции чтения пользователей.
Клиенты, которым нужно лишь читать (стратегии аутентификации, просмотр
списка пользователей), не обязаны зависеть от методов записи.

Принцип стабильных зависимостей (SDP): этот модуль стабилен — он
почти никогда не изменяется. Volatile-компоненты (auth/admin-роутеры,
стратегии) зависят именно от этого стабильного контракта.

Принцип стабильных абстракций (SAP): пакет interfaces/ состоит
исключительно из абстракций, что делает его максимально стабильным.
"""

from abc import ABC, abstractmethod
from typing import List, Optional


class IUserReader(ABC):
    """Контракт только на чтение пользователей (ISP)."""

    @abstractmethod
    def get_by_id(self, user_id: int) -> Optional[object]: ...

    @abstractmethod
    def get_by_email(self, email: str) -> Optional[object]: ...

    @abstractmethod
    def get_by_phone(self, phone: str) -> Optional[object]: ...

    @abstractmethod
    def get_all(self) -> List: ...
