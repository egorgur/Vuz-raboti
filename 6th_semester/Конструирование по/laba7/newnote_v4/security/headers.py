"""Middleware с набором защитных HTTP-заголовков."""

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
  """Добавляет защитные заголовки к каждому ответу."""

    async def dispatch(self, request: Request, call_next) -> Response:
        response: Response = await call_next(request)
        for header, value in SECURITY_HEADERS.items():
            response.headers[header] = value
        return response
