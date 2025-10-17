# services/identity_platform.py
import firebase_admin
from firebase_admin import credentials, auth
from utils.secrets_manager import get_service_account
import requests
from utils.config import FIREBASE_API_KEY

# Initialize Firebase Admin SDK (only once)
def initialize_firebase():
    if not firebase_admin._apps:
        sa_dict = get_service_account()  # 🔹 called at runtime
        # print("Fetched SA:", sa_dict)
        cred = credentials.Certificate(sa_dict)
        firebase_admin.initialize_app(cred)

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