import os
import mysql.connector
from contextlib import contextmanager

# --- Configuration (Auth DB) ---
# DB_HOST will be set based on environment (local=127.0.0.1, production=VM_PRIVATE_IP)
DB_USER = os.environ.get("DB_USER", "auth_user")
DB_PASS = os.environ.get("DB_PASS", "password")
DB_NAME = os.environ.get("DB_NAME", "auth_db")
DB_PORT = os.environ.get("DB_PORT", 3306)
VM_PRIVATE_IP = os.environ.get("DB_HOST") 

# Determine if running in Cloud Run (Production) or Local
# If K_SERVICE is set, we assume production deployment and use the VM_PRIVATE_IP
IS_PRODUCTION = os.environ.get("K_SERVICE") is not None

def get_db_host():
    """Returns the correct database host based on the runtime environment."""
    if IS_PRODUCTION:
        # Production (VM/Cloud Run with VPC Connector): Connect using the VM's Internal IP
        if not VM_PRIVATE_IP:
            raise EnvironmentError("VM_PRIVATE_IP environment variable must be set in production.")
        return VM_PRIVATE_IP
    else:
        # Local Development: Connect using the local SSH Tunnel
        return "127.0.0.1" 

@contextmanager
def get_db_connection():
    """
    Returns a managed raw MySQL connection object.
    The connection is automatically closed upon exiting the 'with' block.
    """
    conn = None
    try:
        conn = mysql.connector.connect(
            host=get_db_host(),
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASS,
            database=DB_NAME,
            # Use cursor dictionary=True for cleaner results (returns dicts, not tuples)
            # but we will handle the cursor separately for flexibility.
        )
        yield conn
    except Exception as e:
        print(f"Database connection error: {e}")
        # Re-raise the exception to be caught by the API handler
        raise
    finally:
        if conn and conn.is_connected():
            conn.close()