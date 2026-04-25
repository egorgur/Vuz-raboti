from fastapi import FastAPI
from database import Base, engine
from routers import auth, notes

Base.metadata.create_all(bind=engine)

app = FastAPI(title="NewNote", description="Simple note-taking web app")

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(notes.router, prefix="/notes", tags=["notes"])
