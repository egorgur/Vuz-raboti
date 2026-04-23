from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta
import random

SECRET_KEY = "change-me-in-production"
ALGORITHM  = "HS256"
TOKEN_EXPIRE_HOURS = 6

pwd_context = CryptContext(schemes=["bcrypt"])


def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(password: str, hashed: str) -> bool:
    return pwd_context.verify(password, hashed)

def create_token(user_id: int) -> str:
    expire = datetime.utcnow() + timedelta(hours=TOKEN_EXPIRE_HOURS)
    payload = {"sub": str(user_id), "exp": expire}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def generate_sms_code() -> str:
    return str(random.randint(100000, 999999))
