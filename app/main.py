from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

app = FastAPI()

from app.routes import auth_router

app.include_router(auth_router)

app.mount("/static", StaticFiles(directory="static"), name="static")
