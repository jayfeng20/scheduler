from openai import OpenAI
import os  
import calendar
import datetime
import json 
from dotenv import load_dotenv
load_dotenv()

import lib.funcs as f
import mysql.connector

host = os.environ.get("DB_ENDPOINT")
user = os.environ.get("DB_USERNAME")
pwd = os.environ.get("DB_PASSWORD")
db = os.environ.get("DB_NAME")


db_config = {
    "host": host,
    "user": user,
    "password": pwd,
    "database": db,
    # 'ssl_ca': 'python_scripts/global-bundle.pem'
}

connection = mysql.connector.connect(**db_config)
if connection.is_connected():
    print("Connected to AWS RDS")
    
# Create a cursor to execute SQL queries
cursor = connection.cursor()
use_db_query = f"USE {db}"
cursor.execute(use_db_query)
print(f"Using database {db}")

current_datetime = datetime.datetime.now()
f.insert(task_name='task1', start_time=current_datetime, end_time=current_datetime, cursor=cursor)

if connection.is_connected():
        cursor.close()
        connection.close()
        print("Connection to AWS RDS closed")
