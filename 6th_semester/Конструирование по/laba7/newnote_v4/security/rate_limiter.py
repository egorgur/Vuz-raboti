"""Простое in-memory ограничение частоты запросов."""

import time
from collections import defaultdict
from fastapi import Request, HTTPException

_MAX_ATTEMPTS = 5
_WINDOW_SEC = 60

_attempts: dict[str, list[float]] = defaultdict(list)


def check_rate_limit(request: Request, endpoint: str) -> None:
    """Выбрасывает HTTP 429, если лимит по IP превышен."""
    ip = request.client.host if request.client else "unknown"
    key = f"{ip}:{endpoint}"
    now = time.time()

    _attempts[key] = [t for t in _attempts[key] if t > now - _WINDOW_SEC]

    if len(_attempts[key]) >= _MAX_ATTEMPTS:
        retry_after = int(_WINDOW_SEC - (now - _attempts[key][0]))
        raise HTTPException(
            status_code=429,
            detail=f"Too many attempts. Retry after {retry_after}s.",
            headers={"Retry-After": str(retry_after)},
        )
    _attempts[key].append(now)
