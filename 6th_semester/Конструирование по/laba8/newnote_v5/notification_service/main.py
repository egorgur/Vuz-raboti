"""Сервис отправки уведомлений."""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="NewNote Notification Service", version="2.0")


class NotificationRequest(BaseModel):
    channel: str
    to: str
    message: str


def send_sms(to: str, message: str) -> None:
    print(f"[SMS] → {to}: {message}")


def send_email(to: str, message: str) -> None:
    print(f"[EMAIL] → {to}: {message}")


_CHANNELS = {"sms": send_sms, "email": send_email}


@app.post("/notify")
def notify(data: NotificationRequest):
    sender = _CHANNELS.get(data.channel)
    if not sender:
        raise HTTPException(400, f"Unknown channel: {data.channel}")
    sender(data.to, data.message)
    return {"status": "queued", "channel": data.channel, "to": data.to}


@app.get("/health")
def health():
    return {"status": "ok"}
