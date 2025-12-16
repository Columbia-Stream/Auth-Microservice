# services/identity_platform.py
import firebase_admin
from firebase_admin import credentials, auth
import requests
from utils.config import FIREBASE_API_KEY, PROJECT_ID

# Initialize Firebase Admin SDK (only once)
def initialize_firebase():
    if not firebase_admin._apps:
        creds = credentials.ApplicationDefault()
        
        # 2. Initialize the app, passing in both the
        #    credentials AND your Project ID.
        firebase_admin.initialize_app(creds, {
            'projectId': PROJECT_ID,
        })

def create_user_in_identity_platform(email: str, password: str):
    """
    Creates a user in Google Identity Platform using Firebase Admin SDK.
    """
    initialize_firebase()
    user_record = auth.create_user(
        email=email,
        password=password
    )
    return user_record


def delete_user_from_identity_platform(uid: str):
    """
    Deletes a user from Google Identity Platform using their User ID (UID).
    
    Args:
        uid: The unique identifier (UID) of the user to delete.
    """
    initialize_firebase()
    
    try:
        # 1. Check if the user exists (optional, but good for clear error handling)
        # auth.get_user(uid) 
        
        # 2. Delete the user
        auth.delete_user(uid)
        print(f"Successfully deleted user with UID: {uid}")
        return True
        
    except auth.UserNotFoundError:
        print(f"Error: User with UID {uid} not found.")
        return False
        
    except Exception as e:
        print(f"An error occurred while deleting user {uid}: {e}")
        return False

def set_user_role_in_identity_platform(uid: str, role: str):
    """
    Sets custom claims (like roles) for a user in Google Identity Platform.
    """
    initialize_firebase()
    auth.set_custom_user_claims(uid, {'role': role})

def login_user(email: str, password: str):
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={FIREBASE_API_KEY}"
    payload = {
        "email": email,
        "password": password,
        "returnSecureToken": True
    }
    response = requests.post(url, json=payload)
    print("Login response:", response.text)
    data = response.json()
    if "idToken" in data:
        return {"idToken": data["idToken"], "email": data["email"]}
    else:
        raise Exception(data.get("error", "Login failed"))

def verify_token(id_token: str):
    try:
        initialize_firebase()
        decoded_token = auth.verify_id_token(id_token)
        return decoded_token  # Contains uid, email, etc.
    except Exception as e:
        raise Exception("Invalid or expired token")