from fastapi import FastAPI, Depends, Request, HTTPException
from sqlalchemy.orm import Session

import crud
from database import get_db, init_db
import string
import random
from cache import is_rate_limited
from fastapi.staticfiles import StaticFiles


app = FastAPI()

app.mount("/", StaticFiles(directory="static", html=True), name="static")


@app.on_event("startup")
def startup():
    init_db()


def generate_code(length=6):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))


@app.post("/shorten")
def shorten(request: Request, url: str, db: Session = Depends(get_db)):
    client_ip = request.client.host
    if is_rate_limited(client_ip):
        raise HTTPException(status_code=429, detail="Too many requests")

    code = generate_code()
    while crud.short_code_exists(db, code):
        code = generate_code()

    return crud.create_short_url(db, url, code)


@app.get("/{short_code}")
def redirect(short_code: str, db: Session = Depends(get_db)):
    original = crud.get_original_url(db, short_code)
    if not original:
        raise HTTPException(status_code=404, detail="Short URL not found")
    return {"original_url": original}
