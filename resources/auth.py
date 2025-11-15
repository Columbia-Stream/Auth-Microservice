# resources/auth.py
from fastapi import APIRouter, HTTPException, Header
from services.identity_platform import (
    create_user_in_identity_platform,
    login_user,
    verify_token,
    set_user_role_in_identity_platform,
)
from models.auth import SignupRequest, LoginRequest

router = APIRouter()
ROLE_ROUTES = {
    "student": "/dashboard/student",
    "faculty": "/dashboard/faculty"
}

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

        set_user_role_in_identity_platform(user_record.uid, user.role)

        return {
            "uid": user_record.uid,
            "email": user_record.email,
            "role": user.role
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/login")
def login(user: LoginRequest):
    """
    Endpoint to log in a user and return an ID token.
    """
    try:
        auth_response = login_user(email=user.email, password=user.password)
        decoded_token = verify_token(auth_response["idToken"])
        role = decoded_token.get("role")
        dashboard_route = ROLE_ROUTES.get(role, "/dashboard")
        return {
            "id_token": auth_response["idToken"],
            "email": auth_response["email"],
            "role": role,
            "dashboard_route": dashboard_route
        }
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
        role = decoded_token.get("role")
        dashboard_route = ROLE_ROUTES.get(role, "/dashboard")
        return {
            "message": "Access granted",
            "uid": decoded_token["uid"],
            "role": role,
            "dashboard_route": dashboard_route
        }
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))
    
