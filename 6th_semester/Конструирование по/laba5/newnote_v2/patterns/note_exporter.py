"""Фабрика экспортёров заметок."""

from __future__ import annotations
from abc import ABC, abstractmethod
import json
from models import Note


class NoteExporter(ABC):
    """Базовый интерфейс экспортёра."""

    @abstractmethod
    def export(self, note: Note) -> str:
        """Преобразует заметку в строку."""
        ...

    @property
    @abstractmethod
    def content_type(self) -> str: ...


class PlainTextExporter(NoteExporter):
    """Экспорт в обычный текст."""

    def export(self, note: Note) -> str:
        return (
            f"Title: {note.title}\n"
            f"Created: {note.created_at}\n"
            f"Updated: {note.updated_at}\n\n"
            f"{note.text}"
        )

    @property
    def content_type(self) -> str:
        return "text/plain"


class JsonExporter(NoteExporter):
    """Экспорт в JSON."""

    def export(self, note: Note) -> str:
        return json.dumps(
            {
                "id": note.id,
                "title": note.title,
                "text": note.text,
                "created_at": str(note.created_at),
                "updated_at": str(note.updated_at),
            },
            ensure_ascii=False,
            indent=2,
        )

    @property
    def content_type(self) -> str:
        return "application/json"


class NoteExporterFactory(ABC):
    """Базовая фабрика экспортёров."""

    @abstractmethod
    def create_exporter(self) -> NoteExporter:
        """Создаёт объект экспортёра."""
        ...

    def get_export(self, note: Note) -> tuple[str, str]:
        """Возвращает данные экспорта и тип контента."""
        exporter = self.create_exporter()
        return exporter.export(note), exporter.content_type


class PlainTextExporterFactory(NoteExporterFactory):
    """Фабрика текстового экспортёра."""

    def create_exporter(self) -> NoteExporter:
        return PlainTextExporter()


class JsonExporterFactory(NoteExporterFactory):
    """Фабрика JSON-экспортёра."""

    def create_exporter(self) -> NoteExporter:
        return JsonExporter()


_FACTORIES: dict[str, NoteExporterFactory] = {
    "txt": PlainTextExporterFactory(),
    "json": JsonExporterFactory(),
}


def get_exporter_factory(fmt: str) -> NoteExporterFactory:
    """Возвращает фабрику по имени формата."""
    factory = _FACTORIES.get(fmt)
    if factory is None:
        raise ValueError(
            f"Unknown export format: {fmt!r}. Supported: {list(_FACTORIES)}"
        )
    return factory
