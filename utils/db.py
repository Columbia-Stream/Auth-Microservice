import mysql.connector
import os
from dotenv import load_dotenv
from utils.config import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME, DB_PORT

load_dotenv()  # loads DB_HOST, DB_USER, DB_PASS, DB_NAME

def test_connection():
    try:
        connection = mysql.connector.connect(
            port=3306,
            user='microuser',
            host='34.55.37.57',
            password='SecurePass123',
            database='Project_SQL'
        )
        if connection.is_connected():
            print("✅ Successfully connected to the DB")
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
            print("⚠️ Connection object created but not connected")
        connection.close()
    except Exception as e:
        print("❌ DB connection failed:", e)
