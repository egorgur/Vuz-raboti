"""
Аспект безопасности №1: Ограничение частоты запросов (Rate Limiting).

Назначение: защита эндпоинтов аутентификации от атак перебором пароля
(brute-force) и SMS-флудинга.

Компромисс с производительностью: in-memory хранилище исключает
сетевой overhead, но ограничивает работу одним процессом. Для MVP
(≤500 одновременных пользователей, 1 узел) это приемлемо.

Компромисс с доступностью: легитимный пользователь, допустивший
5 ошибок подряд, блокируется на 60 секунд. Это компромисс в пользу
безопасности: блокировка кратковременна и применяется только к IP.
"""

import time
from collections import defaultdict
from fastapi import Request, HTTPException

_MAX_ATTEMPTS = 5
_WINDOW_SEC   = 60

_attempts: dict[str, list[float]] = defaultdict(list)


def check_rate_limit(request: Request, endpoint: str) -> None:
    """Бросает HTTP 429, если IP превысил лимит для данного эндпоинта."""
    ip  = request.client.host if request.client else "unknown"
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
