# resources/auth.py
from fastapi import APIRouter, HTTPException, Header
from services.identity_platform import create_user_in_identity_platform, login_user, verify_token
from models.auth import SignupLoginRequest

router = APIRouter()

@router.post("/signup")
async def signup(user: SignupLoginRequest):
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

@router.post("/login")
def login(user: SignupLoginRequest):
    """
    Endpoint to log in a user and return an ID token.
    """
    try:
        auth_response = login_user(email=user.email, password=user.password)
        return {"id_token": auth_response["idToken"], "email": auth_response["email"]}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/verify-token")
def protect(authorization: str = Header(...)):
    """
    Expects Authorization: Bearer <id_token>
    """
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid auth header")
    
    id_token = authorization.split(" ")[1]
    
    try:
        decoded_token = verify_token(id_token)
        return {"message": "Access granted", "uid": decoded_token["uid"]}
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))
    
