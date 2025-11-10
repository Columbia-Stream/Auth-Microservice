# test_firebase.py
import firebase_admin
from firebase_admin import credentials
import sys
import os
PROJECT_ID = "qualified-root-474022-u3"
# --- Make sure this import path is correct ---
# This assumes your config.py is in a folder named 'utils'
# in the same directory as this test file.
# try:
#     from utils.config import PROJECT_ID
# except ImportError:
#     print("ERROR: Could not import PROJECT_ID from utils.config.")
#     print("Please make sure utils/config.py exists and is correct.")
#     sys.exit(1)

print("--- STARTING TEST ---")
print(f"Python version: {sys.version.split()[0]}")
print(f"Project ID from config: {PROJECT_ID}")

# Check for the old env variable, just in case
if "GOOGLE_APPLICATION_CREDENTIALS" in os.environ:
    print("WARNING: GOOGLE_APPLICATION_CREDENTIALS is set. This might override the test.")

try:
    print("Attempting to load ApplicationDefault credentials...")
    creds = credentials.ApplicationDefault()
    print("Credentials loaded successfully.")

    print("Attempting to initialize Firebase app...")
    firebase_admin.initialize_app(creds, {
        'projectId': PROJECT_ID,
    })

    print("\n" + "*"*20)
    print("--- SUCCESS! ---")
    print("Firebase initialized successfully without crashing.")
    print("*"*20)

except Exception as e:
    print("\n" + "!"*20)
    print("--- TEST FAILED WITH AN ERROR ---")
    import traceback
    traceback.print_exc() # This will print the full error stack trace
    print("!"*20)

print("--- TEST COMPLETE ---")