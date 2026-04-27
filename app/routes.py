from .main import cursor,conn, password_helper
from typing import Annotated
from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates


templates = Jinja2Templates(directory="templates")
auth_router = APIRouter(prefix="/auth", tags=["auth"])

@auth_router.get("/register", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse(
        request,
        "item.html"
    )

@auth_router.post("/register")
def create_user(
    name: Annotated[str, Form()],
    email: Annotated[str, Form()],
    password: Annotated[str, Form()]):
    try:
        hashed_password = password_helper.hash(password)
        cursor.execute("""INSERT INTO players (name, email, password) VALUES (%s, %s, %s) RETURNING * """, (name, email, hashed_password))

        new_player = cursor.fetchone()

        conn.commit()

        return RedirectResponse(url="/auth/login", status_code=303)
    except TypeError as e:
        return{"error": f"Error {e}"}