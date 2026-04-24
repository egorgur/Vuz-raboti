"""
Паттерн проектирования: Фабричный метод (Factory Method) — порождающий.

Контекст: Систему планируется расширять форматами экспорта заметок
(plain text, JSON, Markdown и т.д.). Если создавать экспортёры напрямую
в роутере через ветвление (if/elif), то при добавлении нового формата
придётся изменять роутер, нарушая принцип Open/Closed.
Фабричный метод выносит логику создания конкретного экспортёра в
отдельный метод, который подклассы переопределяют самостоятельно.

Когда НЕ использовать Абстрактную фабрику (Abstract Factory):
Абстрактная фабрика нужна, когда порождаются семейства взаимосвязанных
объектов (например, кнопка + форма + диалог для одной темы UI).
Здесь создаётся только один тип объекта — экспортёр. Поэтому
Фабричный метод достаточен и не несёт излишней сложности.

Когда НЕ использовать Строитель (Builder):
Строитель нужен для пошагового создания сложного объекта с многими
параметрами. Экспортёры здесь просты и не требуют пошаговой сборки.
"""

from __future__ import annotations
from abc import ABC, abstractmethod
import json
from models import Note


# ── Product interface ─────────────────────────────────────────────────────────

class NoteExporter(ABC):
    """Абстрактный продукт: экспортёр заметки."""

    @abstractmethod
    def export(self, note: Note) -> str:
        """Сериализует заметку в строку нужного формата."""
        ...

    @property
    @abstractmethod
    def content_type(self) -> str: ...


# ── Concrete Products ─────────────────────────────────────────────────────────

class PlainTextExporter(NoteExporter):
    """Конкретный продукт: экспорт в обычный текст."""

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
    """Конкретный продукт: экспорт в JSON."""

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


# ── Creator (Factory) ─────────────────────────────────────────────────────────

class NoteExporterFactory(ABC):
    """Абстрактный создатель: объявляет фабричный метод."""

    @abstractmethod
    def create_exporter(self) -> NoteExporter:
        """Фабричный метод: возвращает конкретный экспортёр."""
        ...

    def get_export(self, note: Note) -> tuple[str, str]:
        """Шаблонный метод: создаёт экспортёр и экспортирует заметку."""
        exporter = self.create_exporter()
        return exporter.export(note), exporter.content_type


class PlainTextExporterFactory(NoteExporterFactory):
    """Конкретный создатель: производит PlainTextExporter."""

    def create_exporter(self) -> NoteExporter:
        return PlainTextExporter()


class JsonExporterFactory(NoteExporterFactory):
    """Конкретный создатель: производит JsonExporter."""

    def create_exporter(self) -> NoteExporter:
        return JsonExporter()


# ── Registry helper ───────────────────────────────────────────────────────────

_FACTORIES: dict[str, NoteExporterFactory] = {
    "txt":  PlainTextExporterFactory(),
    "json": JsonExporterFactory(),
}


def get_exporter_factory(fmt: str) -> NoteExporterFactory:
    """Возвращает фабрику по названию формата (txt / json)."""
    factory = _FACTORIES.get(fmt)
    if factory is None:
        raise ValueError(f"Unknown export format: {fmt!r}. Supported: {list(_FACTORIES)}")
    return factory
