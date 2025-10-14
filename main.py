#source venv/bin/activate
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from resources import auth

from services.identity_platform import login_user
from utils.db import test_connection

app = FastAPI(title="Auth Service")

origins = [
    # IMPORTANT: Replace this with the exact URL of your frontend
    "http://localhost:3000", 
    "http://127.0.0.1:3000",
    
    # If using your VM's IP for Postman/Testing (optional, but good for local checks)
    
    # You can add the production domain of your frontend here later (e.g., "https://my-frontend.com")
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,              # Specify allowed origins
    allow_credentials=True,             # Allow cookies/authorization headers
    allow_methods=["*"],                # Allow all methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],                # Allow all headers (Content-Type, Authorization, etc.)
)


app.include_router(auth.router, prefix="/auth", tags=["Auth"])


@app.get("/test-db")
def test_db():
    test_connection()
    return {"message": "DB test executed"}

