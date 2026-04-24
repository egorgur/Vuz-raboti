"""
Пакет security/ — аспекты безопасности системы NewNote.

Содержит три компонента:
  - rate_limiter.py   : защита от brute-force (Rate Limiting);
  - headers_middleware.py : HTTP заголовки безопасности;
  - rbac.py           : ролевая модель доступа (RBAC).
"""
