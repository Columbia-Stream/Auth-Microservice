from typing import Literal
from pydantic import BaseModel, EmailStr


class SignupRequest(BaseModel):
    email: EmailStr        # ensures valid email format
    password: str
    role: Literal["student", "faculty"]


class LoginRequest(BaseModel):
    email: EmailStr
    password: str
