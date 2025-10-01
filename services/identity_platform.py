# services/identity_platform.py
import firebase_admin
from firebase_admin import credentials, auth
from utils.secrets_manager import get_service_account

# Initialize Firebase Admin SDK (only once)
def initialize_firebase():
    if not firebase_admin._apps:
        sa_dict = get_service_account()  # 🔹 called at runtime
        print("Fetched SA:", sa_dict)
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
