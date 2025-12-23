from fastapi import FastAPI, Request, Form, Response, HTTPException, Depends, status
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse
import crypto
import random

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Хранилище (в памяти)
users = {"admin": "1234"}
notes = []  # Список dict: {"id": int, "user": str, "content": str}
server_private_key = random.randint(1000, 1000000)
server_public_key = pow(crypto.G, server_private_key, crypto.P)


def get_current_user(request: Request):
    session = request.cookies.get("session")
    if not session:
        return None
    try:
        return crypto.decrypt_cookie(session)
    except:
        return None


@app.get("/")
async def home(request: Request, user=Depends(get_current_user)):
    if not user:
        return templates.TemplateResponse("login.html", {"request": request})
    user_notes = [n for n in notes if n["user"] == user]
    return templates.TemplateResponse(
        "notes.html", {"request": request, "user": user, "notes": user_notes}
    )


@app.get("/dh-params")
async def get_dh_params():
    return {"p": hex(crypto.P), "g": crypto.G, "pub": hex(server_public_key)}


@app.post("/login")
async def login(username: str = Form(...), password: str = Form(...)):
    if users.get(username) == password:
        content = {"message": "ok"}
        response = JSONResponse(content=content)
        response.set_cookie(
            key="session", value=crypto.encrypt_cookie(username), httponly=True
        )
        return response
    raise HTTPException(status_code=401)


@app.post("/notes/add")
async def add_note(request: Request, user=Depends(get_current_user)):
    if not user:
        raise HTTPException(403)

    data = await request.json()  # Ожидаем {client_pub: str, encrypted_content: str}
    client_pub = int(data["client_pub"], 16)

    # DH: Вычисляем секрет K = B^a mod p
    shared_secret = pow(client_pub, server_private_key, crypto.P)
    aes_key = crypto.derive_aes_key(shared_secret)

    # Расшифровываем
    decrypted_text = crypto.decrypt_payload(data["encrypted_content"], aes_key)

    notes.append({"id": len(notes), "user": user, "content": decrypted_text})
    return {"status": "added"}


@app.delete("/notes/{note_id}")
async def delete_note(note_id: int, user=Depends(get_current_user)):
    global notes
    notes = [n for n in notes if not (n["id"] == note_id and n["user"] == user)]
    return {"status": "deleted"}
