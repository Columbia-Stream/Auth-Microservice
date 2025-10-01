#source venv/bin/activate
from fastapi import FastAPI
from resources import auth

app = FastAPI(title="Auth Service")
app.include_router(auth.router, prefix="/auth", tags=["Auth"])