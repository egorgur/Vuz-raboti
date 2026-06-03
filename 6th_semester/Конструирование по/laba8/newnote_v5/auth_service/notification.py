import os
import httpx

NOTIFICATION_SERVICE_URL = os.getenv("NOTIFICATION_SERVICE_URL", "http://notification-service:8003")


def notify(channel: str, to: str, message: str) -> None:
    payload = {"channel": channel, "to": to, "message": message}
    try:
        httpx.post(f"{NOTIFICATION_SERVICE_URL}/notify", json=payload, timeout=5.0)
    except httpx.HTTPError as e:
        print(f"[notification] delivery failed: {e}")
