import sys
import os

# Adjust path to the project root
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

import mysql
from database.query import create_db_connection , fetch_row_by_PRIMARY_KEY , create_table

def connect_to_database():
    DB_HOST = 'mysql-374f4726-majidnamiiiii-e945.a.aivencloud.com'
    DB_PORT = '11741'
    DB_USER = 'avnadmin'
    DB_PASSWORD = 'AVNS_QXs1v9qBTveDtLIXZfW'
    DB_NAME = 'defaultdb'
    
    connection = create_db_connection(DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME)
    return connection

def create_custom_table(mydb, create_table_query):

    create_table(mydb, create_table_query)



# Function to add a new PersianWord
def add_persian_word(mydb, word, frequency=0):
    cursor = mydb.cursor()
    query = "INSERT INTO group1_persianword (word, frequency) VALUES (%s, %s)"
    try:
        cursor.execute(query, (word, frequency))
        mydb.commit()
        print(f"Persian word '{word}' added successfully.")
    except mysql.Error as err:
        print(f"Failed to add Persian word: {err}")
    finally:
        cursor.close()


# Function to get all Persian words
def get_all_persian_words(mydb):
    cursor = mydb.cursor(dictionary=True)
    query = "SELECT * FROM group1_persianword"
    cursor.execute(query)
    words = cursor.fetchall()
    cursor.close()
    return words


# Function to get UserHistory by user_id and word_id
def get_user_history(mydb, user_id, word_id):
    cursor = mydb.cursor(dictionary=True)
    query = "SELECT * FROM group1_userhistory WHERE user_id = %s AND word_id = %s"
    cursor.execute(query, (user_id, word_id))
    history = cursor.fetchall()
    cursor.close()
    return history


# Function to add a new UserHistory record
def add_user_history(mydb, user_id, word_id):
    cursor = mydb.cursor()
    query = "INSERT INTO group1_userhistory (user_id, word_id) VALUES (%s, %s)"
    try:
        cursor.execute(query, (user_id, word_id))
        mydb.commit()
        print(f"User history for user_id '{user_id}' and word_id '{word_id}' added successfully.")
    except mysql.Error as err:
        print(f"Failed to add user history: {err}")
    finally:
        cursor.close()


# Function to fetch a Persian word by its ID
def get_persian_word_by_id(mydb, word_id):
    return fetch_row_by_PRIMARY_KEY(mydb, "group1_persianword", word_id)


# Function to fetch a UserHistory record by its ID
def get_user_history_by_id(mydb, history_id):
    return fetch_row_by_PRIMARY_KEY(mydb, "group1_userhistory", history_id)



if __name__ == "__main__":
    
    db_connection = connect_to_database()

    query = """CREATE TABLE IF NOT EXISTS group1_persianword (
        id BIGINT AUTO_INCREMENT PRIMARY KEY,
        word VARCHAR(100) UNIQUE NOT NULL,
        frequency INT DEFAULT 0
    );"""
    create_custom_table(db_connection,query)

    # # Example: Adding a new Persian word
    # add_persian_word(db_connection, "کتاب", 10)

    # # Example: Fetching all Persian words
    # words = get_all_persian_words(db_connection)
    # print(words)

    # # Example: Fetching user history for a given user and word
    # user_history = get_user_history(db_connection, 1, 1)  # Replace with actual user_id and word_id
    # print(user_history)

    # # Example: Adding a new user history record
    # add_user_history(db_connection, 1, 1)  # Replace with actual user_id and word_id

