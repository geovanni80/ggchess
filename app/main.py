from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import psycopg2
from psycopg2.extras import RealDictCursor
import os
from dotenv import load_dotenv
from pwdlib import PasswordHash
from time import sleep

load_dotenv()

db_host = os.getenv("DB_HOST")
db_user = os.getenv("DB_USER")
db_pass = os.getenv("DB_PASS")
db_name = os.getenv("DB_NAME")

app = FastAPI()

password_helper = PasswordHash.recommended()

while True:

    try:
        conn = psycopg2.connect(host=db_host, database=db_name,
        user = db_user, password=db_pass, cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database conection was sucessful")
        break
    except Exception as error:
        print("Connecting to database failed")
        print("Error: ", error)
        sleep(3)


from app.routes import auth_router

app.include_router(auth_router)

app.mount("/static", StaticFiles(directory="static"), name="static")
