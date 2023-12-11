import datetime
import funcs as f
import mysql.connector

# Replace with your RDS endpoint, database name, username, and password
db_config = {
    "host": "your-rds-endpoint.amazonaws.com",
    "user": "your_username",
    "password": "your_password",
    "database": "your_database_name"
}

try:
    connection = mysql.connector.connect(**db_config)
    if connection.is_connected():
        print("Connected to AWS RDS")
        
    # Create a cursor to execute SQL queries
    cursor = connection.cursor()

    # Execute SQL queries here (e.g., SELECT, INSERT, UPDATE)

except mysql.connector.Error as e:
    print(f"Error connecting to AWS RDS: {e}")
finally:
    if connection.is_connected():
        cursor.close()
        connection.close()
        print("Connection to AWS RDS closed")

