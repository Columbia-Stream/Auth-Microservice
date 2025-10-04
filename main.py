#source venv/bin/activate
from fastapi import FastAPI
from resources import auth

from services.identity_platform import login_user
from utils.db import test_connection


app = FastAPI(title="Auth Service")
app.include_router(auth.router, prefix="/auth", tags=["Auth"])


@app.get("/test-db")
def test_db():
    test_connection()
    return {"message": "DB test executed"}

