# resources/auth.py
from fastapi import APIRouter, HTTPException
from services.identity_platform import create_user_in_identity_platform
from models.auth import SignupRequest

router = APIRouter()

@router.post("/signup")
async def signup(user: SignupRequest):
    """
    Endpoint to create a new user in Identity Platform.
    """
    try:
        user_record = create_user_in_identity_platform(
            email=user.email,
            password=user.password
        )
        return {
            "uid": user_record.uid,
            "email": user_record.email
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
