import datetime
import os  
import funcs as f
import mysql.connector



# sql config
host = os.environ.get("DB_ENDPOINT")
user = os.environ.get("DB_USERNAME")
pwd = os.environ.get("DB_PASSWORD")
db = os.environ.get("DB_NAME")

db_config = {
    "host": host,
    "user": user,
    "password": pwd,
    "database": db
}

# create tables
def create(week):
    time = f.start_of_week()
    create_table_query1 = f"""
    CREATE TABLE IF NOT EXISTS {time['month0']+time['day0']+time['year0']} (
        id INT AUTO_INCREMENT PRIMARY KEY,
        task_name VARCHAR(255) NOT NULL,
        start_time DATETIME,
        end_time DATETIME
    )
    """
    cursor.execute(create_table_query1)

    create_table_query2 = f"""
    CREATE TABLE IF NOT EXISTS {time['month1']+time['day1']+time['year1']} (
        id INT AUTO_INCREMENT PRIMARY KEY,
        task_name VARCHAR(255) NOT NULL,
        start_time DATETIME,
        end_time DATETIME
    )
    """
    cursor.execute(create_table_query2)

def insert(slots):


try:
    connection = mysql.connector.connect(**db_config)
    if connection.is_connected():
        print("Connected to AWS RDS")
        
    # Create a cursor to execute SQL queries
    cursor = connection.cursor()

    use_db_query = f"USE {db}"
    cursor.execute(use_db_query)
    print(f"Using database {db}")



except mysql.connector.Error as e:
    print(f"Error connecting to AWS RDS: {e}")
finally:
    if connection.is_connected():
        cursor.close()
        connection.close()
        print("Connection to AWS RDS closed")

