"""
Notification Service — микросервис уведомлений.

Ответственность: отправка SMS и email-уведомлений.
В production подписывается на очередь сообщений (RabbitMQ/Redis Pub/Sub).
В MVP предоставляет HTTP-эндпоинт для вызова из других сервисов.
"""

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="NewNote Notification Service", version="2.0")


class NotificationRequest(BaseModel):
    channel: str   # "sms" | "email"
    to:      str   # телефон или email
    message: str


@app.post("/notify")
def notify(data: NotificationRequest):
    """
    Точка входа для отправки уведомления.
    В production: публикует сообщение в очередь (RabbitMQ).
    В MVP: логирует сообщение.
    """
    # TODO: интегрировать SMS-провайдер (Twilio) и SMTP-сервер
    print(f"[{data.channel.upper()}] → {data.to}: {data.message}")
    return {"status": "queued", "channel": data.channel, "to": data.to}


@app.get("/health")
def health():
    return {"status": "ok"}
