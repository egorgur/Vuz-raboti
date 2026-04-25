"""API Gateway: прокси между клиентом и микросервисами."""

import httpx
from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError

SECRET_KEY = "change-me-in-production"
ALGORITHM = "HS256"

AUTH_SERVICE_URL = "http://auth-service:8001"
NOTES_SERVICE_URL = "http://notes-service:8002"

app = FastAPI(title="NewNote API Gateway")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login", auto_error=False)


def verify_token(token: str) -> dict:
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")


async def proxy(url: str, request: Request, extra_headers: dict = None) -> JSONResponse:
    headers = dict(request.headers)
    if extra_headers:
        headers.update(extra_headers)
    async with httpx.AsyncClient() as client:
        resp = await client.request(
            method=request.method,
            url=url,
            headers=headers,
            content=await request.body(),
            params=request.query_params,
            timeout=10.0,
        )
    return JSONResponse(
        status_code=resp.status_code, content=resp.json() if resp.content else {}
    )


@app.api_route("/auth/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def auth_proxy(path: str, request: Request):
    """Проксирует запрос в auth-service."""
    return await proxy(f"{AUTH_SERVICE_URL}/auth/{path}", request)


@app.api_route("/notes/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def notes_proxy(
    path: str,
    request: Request,
    token: str = Depends(oauth2_scheme),
):
    """Проксирует запрос в notes-service после проверки токена."""
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    payload = verify_token(token)
    user_id = payload.get("sub")
    role = payload.get("role", "user")
    return await proxy(
        f"{NOTES_SERVICE_URL}/notes/{path}",
        request,
        extra_headers={"X-User-Id": str(user_id), "X-User-Role": role},
    )
