"""
Auth Service — микросервис аутентификации.

Ответственность:
  - регистрация пользователей;
  - вход по e-mail/паролю;
  - вход по SMS OTP;
  - выдача и проверка JWT-токенов.

Имеет собственную базу данных (auth.db).
"""

from fastapi import FastAPI
from auth_service.database import Base, engine
from auth_service.router import router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="NewNote Auth Service", version="2.0")
app.include_router(router, prefix="/auth")
