# resources/auth.py
from fastapi import APIRouter, HTTPException, Header, status
from services.identity_platform import create_user_in_identity_platform, login_user, verify_token, delete_user_from_identity_platform
from models.auth import SignupRequest, LoginRequest, UpdateRoleRequest
from utils.sql import get_all_users_from_db, insert_in_db, get_user_from_db_email, get_user_from_db_uni, update_db, get_profs_from_db


router = APIRouter()
ROLE_ROUTES = {
    "student": "/dashboard/student",
    "faculty": "/dashboard/faculty"
}

@router.post("/signup", status_code=status.HTTP_201_CREATED)
async def signup(user: SignupRequest):
    """
    Endpoint to create a new user in Identity Platform.
    """
    try:
        user_record = create_user_in_identity_platform(
            email=user.email,
            password=user.password
        )
        # Also insert user details into the database
        # set_user_role_in_identity_platform(user_record.uid, user.role)
        insert_in_db(
            email=user.email,
            password=user.password,
            uni=user.uni,
            role=user.role
        )
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
        
        db_results = get_user_from_db_email(email=user.email)
        role = db_results[0]["role"]
        dashboard_route = ROLE_ROUTES.get(role, "/dashboard")

        if not db_results:
            raise HTTPException(status_code=404, detail="User not found in database")
        
        return {"id_token": auth_response["idToken"], "email": auth_response["email"], "role": role, "uni": db_results[0]["uni"], "dashboard_route": dashboard_route}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/handle-oauth", status_code=status.HTTP_201_CREATED)
async def google_auth(authorization: str = Header(None)):
    """
    Endpoint to create a new user in Identity Platform.
    """
    try:
        print("Authorization Header:")
        if not authorization:
            print("No Authorization header provided")
            raise HTTPException(status_code=401, detail="Missing Authorization header")

        # Expect format: "Bearer <token>"
        if not authorization.startswith("Bearer "):
            print("No Authorization header provided 2")
            raise HTTPException(status_code=401, detail="Invalid Authorization header")

        # Extract token
        id_token = authorization.split(" ")[1]
        print("Received ID Token:", id_token)
        # if not columbia.edu and barnard.edu - delete user and return proper response
        # if user exists in db
        # if user does not exist in db - create user with student role
        claims = verify_token(id_token)
        print("Token Claims:", claims)
        # Claims is a dictionary containing the payload data:
        user_uid = claims.get('uid')
        user_email = claims.get('email')
        
        print(f"Token verified! UID: {user_uid}, Email: {user_email}")
        if(not user_email.endswith("@columbia.edu") and not user_email.endswith("@barnard.edu")):
            # delete user from identity platform
            try:
                delete_user_from_identity_platform(user_uid)
                print(f"Deleted user with UID: {user_uid} due to unauthorized email domain.")
            except Exception as e:
                print(f"Error deleting user with UID: {user_uid}: {e}")
            raise HTTPException(status_code=403, detail="Unauthorized email domain")
        
        #check if user exists in db
        db_results = get_user_from_db_email(email=user_email)
        

        if not db_results:
            insert_in_db(
                email=user_email,
                password='OAUTH_USER',
                uni=user_email.split('@')[0],
                role='student'
            )
            return {"id_token": id_token, "email": user_email, "role": 'student', "uni": user_email.split('@')[0], "dashboard_route": ROLE_ROUTES.get('student', "/dashboard")}
        else:
            role = db_results[0]["role"]
            dashboard_route = ROLE_ROUTES.get(role, "/dashboard")
            
            return {"id_token": id_token, "email": user_email, "role": role, "uni": db_results[0]["uni"], "dashboard_route": dashboard_route}
    
    except Exception as e:
        print(f"Error in Google OAuth handling: {e}")
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
        print("Decoded Token:", decoded_token)
        db_results = get_user_from_db_email(email=decoded_token.get("email"))
        if not db_results:
            raise HTTPException(status_code=404, detail="User not found in database")
        role = db_results[0]["role"]
        print("User Role from DB:", role, db_results)
        if role not in ROLE_ROUTES:
            raise HTTPException(status_code=403, detail="Unauthorized role")
        dashboard_route = ROLE_ROUTES.get(role, "/dashboard")
        return {"message": "Access granted", "uid": decoded_token["uid"], "role": role, "dashboard_route": dashboard_route}
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))
    
@router.get("/get-user")
def userDetailsUni(uni: str):
    
    try:
        db_results = get_user_from_db_uni(uni=uni)
        return {"message": "User found", "user": db_results}
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))
    
@router.put("/update-role")
def update_role(user: UpdateRoleRequest):
    try:
        update_db(email=user.email, role=user.role)
        return {"message": "Profile updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))
    
@router.get("/get-profs")
def profList():
    try:
        db_results = get_profs_from_db()
        return {"message": "Professor List", "list": db_results}
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))
 