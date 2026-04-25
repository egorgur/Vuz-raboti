"""Публичные интерфейсы работы с заметками."""

from .i_note_reader import INoteReader
from .i_note_writer import INoteWriter

__all__ = ["INoteReader", "INoteWriter"]
