"""
Принцип инверсии зависимостей (DIP): UserRepository реализует
стабильные интерфейсы IUserReader и IUserWriter из пакета interfaces/.
Высокоуровневые модули (роутеры, стратегии) зависят от абстракций,
а не от конкретного класса.

Принцип разделения интерфейсов (ISP): чтение и запись разделены на
два контракта — клиент зависит только от того, что ему нужно.

Принцип подстановки Лисков (LSP): UserRepository заменяем любым другим
классом, реализующим те же интерфейсы (например, InMemoryUserRepository
для тестов).

Принцип единственной ответственности (SRP): репозиторий отвечает только
за доступ к данным пользователей. Принцип общего замыкания (CCP): он
находится в пакете users/ — изменяется вместе с моделью User.
"""

from typing import List, Optional
from sqlalchemy.orm import Session

from users.models import User
from interfaces import IUserReader, IUserWriter


class UserRepository(IUserReader, IUserWriter):
    """
    Конкретная реализация репозитория пользователей.
    Реализует оба интерфейса — читателя и писателя (DIP + ISP + LSP).
    """

    def __init__(self, db: Session) -> None:
        self._db = db

    # ── IUserReader ────────────────────────────────────────────────────────────

    def get_by_id(self, user_id: int) -> Optional[User]:
        return self._db.get(User, user_id)

    def get_by_email(self, email: str) -> Optional[User]:
        return self._db.query(User).filter(User.email == email).first()

    def get_by_phone(self, phone: str) -> Optional[User]:
        return self._db.query(User).filter(User.phone == phone).first()

    def get_all(self) -> List[User]:
        return self._db.query(User).all()

    # ── IUserWriter ────────────────────────────────────────────────────────────

    def create(
        self,
        email: str,
        password_hash: Optional[str] = None,
        phone: Optional[str] = None,
        role: str = "user",
    ) -> User:
        user = User(
            email=email,
            phone=phone,
            password_hash=password_hash,
            role=role,
        )
        self._db.add(user)
        self._db.commit()
        self._db.refresh(user)
        return user

    def save(self, user: User) -> User:
        """Фиксирует изменения уже отслеживаемой сущности (например, OTP-код)."""
        self._db.commit()
        self._db.refresh(user)
        return user

    def delete(self, user: User) -> None:
        self._db.delete(user)
        self._db.commit()
