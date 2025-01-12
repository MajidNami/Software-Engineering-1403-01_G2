import sys
import os

# Adjust path to the project root
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

import os
import django
from database.query import create_db_connection  # Import your query functions


# Function to insert Persian words into the database
def insert_persian_words_from_file(file_path):
    # Database credentials
    from FarsiAid_website.secret import DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME

    # Create database connection
    db_connection = create_db_connection(DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME)

    # Read words from file
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            words = file.readlines()

        # Remove duplicates and strip extra spaces
        words = set(word.strip() for word in words if word.strip())

        cursor = db_connection.cursor()
        insert_query = "INSERT INTO group1_persianword (word, frequency) VALUES (%s, %s)"

        # Insert each word into the database
        for word in words:
            try:
                cursor.execute(insert_query, (word, 0))  # Default frequency set to 0
            except Exception as e:
                print(f"Error inserting word '{word}': {e}")

        # Commit changes
        db_connection.commit()
        print("All words inserted successfully!")

    except FileNotFoundError:
        print("The file does not exist.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if db_connection.is_connected():
            db_connection.close()

# Example usage
if __name__ == "__main__":
    file_path = "C:/Users/Arian/Downloads/persian_words_500.txt"  # Replace with your file path
    insert_persian_words_from_file(file_path)
