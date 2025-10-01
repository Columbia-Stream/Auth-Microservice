import os
from dotenv import load_dotenv

# Load variables from .env file
load_dotenv()

# GCP Settings
PROJECT_ID = os.getenv("PROJECT_ID")
SECRET_ID = os.getenv("SECRET_ID")
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

# MySQL Settings
MYSQL_HOST = os.getenv("MYSQL_HOST", "127.0.0.1")
MYSQL_USER = os.getenv("MYSQL_USER", "root")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "")
MYSQL_DB = os.getenv("MYSQL_DB", "auth_db")

# App Settings
APP_ENV = os.getenv("APP_ENV", "development")  # dev/staging/prod
