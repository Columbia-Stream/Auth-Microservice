from utils.db import get_db_connection
from fastapi import HTTPException
from utils.auth_security import hash_password

def get_all_users_from_db():
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor(dictionary=True) # <-- Get dictionary results
            cursor.execute("SELECT * FROM Users;")
            rows = cursor.fetchall()
            return rows
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"DB error: {str(e)}")


def insert_in_db(email, password, uni, role):
    try:
        hashed_pwd = hash_password(password)
        with get_db_connection() as conn:
            cursor = conn.cursor() # <-- Get dictionary results
            query = "INSERT INTO Users (email, password, uni, role) VALUES (%s, %s, %s, %s);"
            cursor.execute(query, (email, hashed_pwd, uni, role))
            conn.commit()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"DB error: {str(e)}")


def get_user_from_db(email=None):
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor(dictionary=True) # <-- Get dictionary results
            cursor.execute("SELECT * FROM Users WHERE email=%s;", (email,))
            rows = cursor.fetchall()
            return rows
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"DB error: {str(e)}")

