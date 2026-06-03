import os
from fastapi import Header, HTTPException
from jose import jwt, JWTError

SECRET_KEY = os.getenv("SECRET_KEY", "change-me-in-production")
ALGORITHM  = "HS256"


class CurrentUser:
    def __init__(self, id: int, role: str):
        self.id   = id
        self.role = role

    @property
    def is_admin(self) -> bool:
        return self.role == "admin"


def current_user(authorization: str = Header(...)) -> CurrentUser:
    if not authorization.startswith("Bearer "):
        raise HTTPException(401, "Missing token")
    token = authorization.split(" ", 1)[1]
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return CurrentUser(int(payload["sub"]), payload.get("role", "user"))
    except (JWTError, KeyError):
        raise HTTPException(401, "Invalid token")
