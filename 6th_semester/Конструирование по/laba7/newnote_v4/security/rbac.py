from fastapi import HTTPException
from users.models import User


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
