import mysql.connector
import os
from dotenv import load_dotenv
from utils.config import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME, DB_PORT

load_dotenv()  # loads DB_HOST, DB_USER, DB_PASS, DB_NAME

def test_connection():
    try:
        connection = mysql.connector.connect(
            port=DB_PORT,
            user=DB_USER,
            host=DB_HOST,
            password=DB_PASSWORD,
            database=DB_NAME,
        )
        if connection.is_connected():
            print("Successfully connected to the DB")
            cursor = connection.cursor(dictionary=True)  # dictionary=True for column
            cursor.execute("SHOW TABLES;")
            print(cursor.fetchall())
            
            cursor.execute("SELECT * FROM Project_SQL.Users")  # fetch first 5 users
            rows = cursor.fetchall()
            print("Sample users from DB:", rows)
            if rows:
                print("Sample users:")
                for row in rows:
                    print(row)
            else:
                print("No users found in the table")
        else:
            print("Connection object created but not connected")
        connection.close()
    except Exception as e:
        print("DB connection failed:", e)


def get_user_role_by_email(email: str):
    """
    Fetches the role for a user identified by email from Project_SQL.Users.
    Returns None if the user does not exist or an error occurs.
    """
    connection = None
    cursor = None
    try:
        connection = mysql.connector.connect(
            port=DB_PORT,
            user=DB_USER,
            host=DB_HOST,
            password=DB_PASSWORD,
            database=DB_NAME,
        )
        cursor = connection.cursor(dictionary=True)
        query = "SELECT role FROM Project_SQL.Users WHERE email = %s LIMIT 1"
        cursor.execute(query, (email,))
        result = cursor.fetchone()
        if result and "role" in result:
            return result["role"]
        return None
    except Exception as e:
        print(f"Failed to fetch role for {email}: {e}")
        return None
    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()


def save_user_role(email: str, role: str):
    """Insert or update a user's role in Project_SQL.Users."""
    if not role:
        raise ValueError("role must be provided")

    connection = None
    cursor = None
    try:
        connection = mysql.connector.connect(
            port=DB_PORT,
            user=DB_USER,
            host=DB_HOST,
            password=DB_PASSWORD,
            database=DB_NAME,
        )
        cursor = connection.cursor()

        update_query = "UPDATE Project_SQL.Users SET role = %s WHERE email = %s"
        cursor.execute(update_query, (role, email))

        if cursor.rowcount == 0:
            insert_query = "INSERT INTO Project_SQL.Users (email, role) VALUES (%s, %s)"
            cursor.execute(insert_query, (email, role))

        connection.commit()
    except Exception as e:
        print(f"Failed to upsert role for {email}: {e}")
        raise
    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()
