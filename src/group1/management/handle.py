import sys
import os

# Adjust path to the project root
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))


import mysql.connector as mysql
from werkzeug.security import generate_password_hash, check_password_hash
from database.query import create_db_connection, save_user


DB_NAME = 'defaultdb'
DB_USER = 'avnadmin'
DB_PASSWORD = 'AVNS_QXs1v9qBTveDtLIXZfW'
DB_HOST = 'mysql-374f4726-majidnamiiiii-e945.a.aivencloud.com'
DB_PORT = '11741'

db_connection = create_db_connection(DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME)



def handle_login(username, password1):
    try:
        cursor = db_connection.cursor(dictionary=True)

        # Check if the user exists
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()

        if not user:
            return "User does not exist. Please register."

        # Verify password
        if user['password'] == password1:
            return "Login successful."
        else:
            return "Invalid password."

    except mysql.Error as e:
        return f"Database error: {e}"
    finally:
        cursor.close()


def handle_register(username, name, email, age, password, confirm_password):
    try:
        cursor = db_connection.cursor(dictionary=True)

        
        
        # Check if the user already exists
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()

        if user:
            return "User already exists. Please login."
        
        if password != confirm_password:
            return "Passwords are not the same!"
        
        # Save the user
        save_user(db_connection, name, username, password, email, age)
        return "Registration successful. Please login."
    
    except mysql.Error as e:
        return f"Database error: {e}"
    finally:
        cursor.close()
