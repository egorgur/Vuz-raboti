"""Сервис отправки уведомлений."""

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="NewNote Notification Service", version="2.0")


class NotificationRequest(BaseModel):
    channel: str
    to: str
    message: str


@app.post("/notify")
def notify(data: NotificationRequest):
    """Ставит уведомление в обработку."""
    print(f"[{data.channel.upper()}] → {data.to}: {data.message}")
    return {"status": "queued", "channel": data.channel, "to": data.to}


@app.get("/health")
def health():
    return {"status": "ok"}
