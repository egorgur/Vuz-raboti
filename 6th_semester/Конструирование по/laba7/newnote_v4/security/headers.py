"""
Аспект безопасности № 3: Защитные HTTP-заголовки (Security Headers Middleware).

Назначение: предотвращение типичных веб-атак через HTTP-заголовки ответа:
  - XSS (Cross-Site Scripting): Content-Security-Policy ограничивает
    источники скриптов только текущим доменом.
  - Clickjacking: X-Frame-Options запрещает встраивание страницы в iframe.
  - MIME sniffing: X-Content-Type-Options запрещает браузеру угадывать
    MIME-тип ответа, что предотвращает выполнение текстовых файлов как JS.
  - Небезопасные соединения: Strict-Transport-Security (HSTS) требует
    HTTPS на протяжении 1 года, включая поддомены.
  - Утечка Referer: Referrer-Policy ограничивает заголовок Referer.

Компромисс (Trade-off):
  + Безопасность: устраняет целый класс атак без изменения
    бизнес-логики и без накладных расходов на производительность.
  - Совместимость: строгая CSP может поломать интеграцию со сторонними
    скриптами (например, аналитика, CDN). Текущая политика 'self'
    блокирует любые внешние скрипты. При необходимости интеграции
    с CDN потребуется явно добавить домен в CSP.
  - Разработка: HSTS с includeSubDomains может мешать локальной
    разработке на HTTP. Принятое решение: middleware применяется
    к production-окружению (переключается через переменную окружения).
"""

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response


SECURITY_HEADERS = {
    "X-Content-Type-Options":    "nosniff",
    "X-Frame-Options":           "DENY",
    "X-XSS-Protection":          "1; mode=block",
    "Referrer-Policy":           "strict-origin-when-cross-origin",
    "Strict-Transport-Security": "max-age=31536000; includeSubDomains",
    "Content-Security-Policy": (
        "default-src 'self'; "
        "script-src 'self'; "
        "style-src 'self' 'unsafe-inline'; "
        "img-src 'self' data:; "
        "frame-ancestors 'none';"
    ),
    "Permissions-Policy": "geolocation=(), microphone=(), camera=()",
}


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """
    Starlette middleware: добавляет защитные HTTP-заголовки к каждому ответу.

    Подключение в main.py:
        app.add_middleware(SecurityHeadersMiddleware)
    """

    async def dispatch(self, request: Request, call_next) -> Response:
        response: Response = await call_next(request)
        for header, value in SECURITY_HEADERS.items():
            response.headers[header] = value
        return response
