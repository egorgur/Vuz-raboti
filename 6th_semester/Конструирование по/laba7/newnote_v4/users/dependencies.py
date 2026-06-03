"""
FastAPI-провайдеры зависимостей для работы с пользователями.

Принцип инверсии зависимостей (DIP): эндпоинты объявляют в сигнатуре
потребность в абстракциях IUserReader / IUserWriter, а конкретная
реализация (UserRepository) подставляется механизмом Depends FastAPI.
Это убирает ручное создание репозитория внутри обработчиков и делает
зависимости легко заменяемыми (например, на in-memory реализацию в тестах
через app.dependency_overrides).
"""

from fastapi import Depends
from sqlalchemy.orm import Session

from database import get_db
from users.repository import UserRepository
from interfaces import IUserReader, IUserWriter


def get_user_reader(db: Session = Depends(get_db)) -> IUserReader:
    return UserRepository(db)


def get_user_writer(db: Session = Depends(get_db)) -> IUserWriter:
    return UserRepository(db)
