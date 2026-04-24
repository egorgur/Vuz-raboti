"""
Аспект безопасности №3: Ролевая модель доступа (RBAC).

Назначение: централизованное управление правами доступа через роли.
В системе NewNote выделены две роли:
  - USER  — обычный пользователь; видит и изменяет только свои заметки;
  - ADMIN — администратор; может просматривать заметки любого пользователя.

Компромисс с производительностью: каждый защищённый запрос выполняет
дополнительную проверку поля role из БД (уже загруженного при
JWT-аутентификации, без лишних запросов к БД). Overhead минимален.

Компромисс с гибкостью: роли хранятся как строковые константы в БД.
При масштабировании до сложной ролевой иерархии (например, RBAC с
наследованием ролей) потребуется отдельная таблица roles. Для MVP
двух ролей достаточно.

Компромисс с нефункциональными требованиями: проверка роли не влияет
на время отклика (≤2 с) и совместима с требованием масштабируемости —
роли хранятся в пользовательской таблице, а не в сессии сервера.
"""

from fastapi import HTTPException
from auth.models import User


class Role:
    USER  = "user"
    ADMIN = "admin"


def require_role(*roles: str):
    """
    Возвращает функцию-проверку: бросает HTTP 403, если роль пользователя
    не входит в допустимые.

    Использование:
        def endpoint(user = Depends(get_current_user)):
            require_role(Role.ADMIN)(user)
    """
    def _check(user: User) -> None:
        if getattr(user, "role", Role.USER) not in roles:
            raise HTTPException(
                status_code=403,
                detail=f"Access denied. Required role: {' or '.join(roles)}.",
            )
    return _check


def is_admin(user: User) -> bool:
    return getattr(user, "role", Role.USER) == Role.ADMIN
