import os
import random
import time
from collections import defaultdict
from datetime import datetime, timedelta

from fastapi import HTTPException, Request
from passlib.context import CryptContext
from jose import jwt

SECRET_KEY = os.getenv("SECRET_KEY", "change-me-in-production")
ALGORITHM  = "HS256"
TOKEN_TTL  = timedelta(hours=6)

_pwd = CryptContext(schemes=["bcrypt"])
_attempts: dict = defaultdict(list)


def hash_password(password: str) -> str:
    return _pwd.hash(password)


def verify_password(password: str, hashed: str) -> bool:
    return _pwd.verify(password, hashed)


def create_token(user_id: int, role: str) -> str:
    payload = {"sub": str(user_id), "role": role, "exp": datetime.utcnow() + TOKEN_TTL}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def generate_otp() -> str:
    return str(random.randint(100000, 999999))


def rate_limit(request: Request, endpoint: str, limit: int = 5, window: int = 60) -> None:
    ip  = request.client.host if request.client else "unknown"
    key = f"{ip}:{endpoint}"
    now = time.time()
    _attempts[key] = [t for t in _attempts[key] if t > now - window]
    if len(_attempts[key]) >= limit:
        raise HTTPException(429, "Too many attempts")
    _attempts[key].append(now)
