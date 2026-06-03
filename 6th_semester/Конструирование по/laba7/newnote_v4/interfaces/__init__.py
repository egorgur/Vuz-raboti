"""
Пакет interfaces/ — стабильные абстракции системы NewNote.

Принцип SAP (Stable Abstractions Principle): этот пакет содержит
только абстрактные классы (интерфейсы). Чем стабильнее пакет,
тем более абстрактным он должен быть.

Принцип ADP (Acyclic Dependencies Principle): зависимости пакетов
образуют направленный ациклический граф (DAG):
    notes/ → interfaces/
    auth/  → interfaces/
    Циклов нет.
"""

from .i_note_reader import INoteReader
from .i_note_writer import INoteWriter
from .i_user_reader import IUserReader
from .i_user_writer import IUserWriter

__all__ = ["INoteReader", "INoteWriter", "IUserReader", "IUserWriter"]
