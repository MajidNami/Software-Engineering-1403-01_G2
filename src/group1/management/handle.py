import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))


import mysql.connector as mysql
from database.query import create_db_connection, save_user


DB_NAME = 'defaultdb'
DB_USER = 'avnadmin'
DB_PASSWORD = 'AVNS_QXs1v9qBTveDtLIXZfW'
DB_HOST = 'mysql-374f4726-majidnamiiiii-e945.a.aivencloud.com'
DB_PORT = '11741'




def handle_login(username, password1):
    try:
        db_connection = create_db_connection(DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME)
        cursor = db_connection.cursor(dictionary=True)

        
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()

        if not user:
            return "User does not exist. Please register."

        
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
        db_connection = create_db_connection(DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME)
        cursor = db_connection.cursor(dictionary=True)

        
        
        
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()

        if user:
            return "User already exists. Please login."
        
        if password != confirm_password:
            return "Passwords are not the same!"
        
        
        save_user(db_connection, name, username, password, email, age)
        return "Registration successful. Please login."
    
    except mysql.Error as e:
        return f"Database error: {e}"
    finally:
        cursor.close()
