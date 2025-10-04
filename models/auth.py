from pydantic import BaseModel, EmailStr

class SignupLoginRequest(BaseModel):
    email: EmailStr        # ensures valid email format
    password: str
