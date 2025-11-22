from pydantic import BaseModel, EmailStr
from typing import Literal
class SignupRequest(BaseModel):
    email: EmailStr        # ensures valid email format
    password: str
    uni: str
    role: Literal["student", "faculty"]

class LoginRequest(BaseModel):
    email: EmailStr        # ensures valid email format
    password: str
