"""
Аспект безопасности №2: Middleware заголовков безопасности (Security Headers).

Назначение: автоматическое добавление HTTP-заголовков безопасности ко
всем ответам сервера. Защищает от:
  - XSS (Cross-Site Scripting) — Content-Security-Policy, X-XSS-Protection;
  - Clickjacking — X-Frame-Options;
  - MIME-sniffing — X-Content-Type-Options;
  - Принуждение к HTTPS — Strict-Transport-Security (HSTS);
  - Утечки реферера — Referrer-Policy.

Компромисс с производительностью: Middleware добавляет несколько строк
к каждому HTTP-ответу. Overhead измеряется единицами микросекунд и
не влияет на нефункциональное требование (время отклика ≤2 с).

Компромисс с функциональностью: заголовок Content-Security-Policy
ограничивает источники скриптов и стилей. При интеграции с внешними
CDN (например, для будущего фронтенда) потребуется расширение политики CSP.
Текущее значение 'self' достаточно для REST API.

Компромисс с HSTS: принудительное перенаправление на HTTPS означает,
что в процессе разработки (localhost, HTTP) браузер может кэшировать
HSTS и блокировать HTTP-соединения. Для разработки max-age установлен
в 0 (отключён); в production переключается на 31536000 (1 год).
"""

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

SECURITY_HEADERS = {
    "X-Content-Type-Options":    "nosniff",
    "X-Frame-Options":           "DENY",
    "X-XSS-Protection":          "1; mode=block",
    "Referrer-Policy":           "strict-origin-when-cross-origin",
    "Content-Security-Policy":   "default-src 'self'",
    # В production заменить на max-age=31536000; includeSubDomains; preload
    "Strict-Transport-Security": "max-age=0",
    "Cache-Control":             "no-store",
}


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """Добавляет заголовки безопасности к каждому HTTP-ответу."""

    async def dispatch(self, request: Request, call_next) -> Response:
        response: Response = await call_next(request)
        for header, value in SECURITY_HEADERS.items():
            response.headers[header] = value
        return response
