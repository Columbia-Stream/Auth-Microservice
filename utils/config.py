import os
from dotenv import load_dotenv

# Load variables from .env file
load_dotenv()

# GCP Settings
PROJECT_ID = os.getenv("PROJECT_ID")
SECRET_ID = os.getenv("SECRET_ID")
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
FIREBASE_API_KEY = os.getenv("FIREBASE_API_KEY")

# MySQL Settings
DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_NAME = os.getenv("DB_NAME", "auth_db")
DB_PORT = os.getenv("DB_PORT", 3306)

# App Settings
APP_ENV = os.getenv("APP_ENV", "development")  # dev/staging/prod
