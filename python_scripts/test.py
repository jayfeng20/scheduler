from openai import OpenAI
import os  
import calendar
import datetime

import lib.funcs as f
import mysql.connector

# variables
current_datetime = datetime.datetime.now()
task_name = ''
task_type = ''
expected_time = 2
assert expected_time <= 24 and 1 <= expected_time
due_in = 1
assert due_in >= 1 and due_in <= 7 # due in at least 1 day and at most 1 week


# mysql config
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

# openai config
key = os.environ.get("OPENAI_API_KEY")
client = OpenAI(
  api_key=key,
)



alr_booked = []

system_message = """
You are a concise and precise assistant. You find the most reasonable time slot(s) to assign this task within the next week
and before the due date.
Your output is in the form of a json object with 2 fields named "start_time" and "end_time" whose contents are 
python datetime objects. They represent the time slot(s) you chose to schedule the task.
"""

user_message = "Can you please find the best time slot(s) for me to do the following task?" + \
f"""
time right now: {current_datetime}
expected time: {expected_time} hours to finish, 
due in: {due_in} days.
Already booked slots are: {', '.join(alr_booked)}.
"""


completion = client.chat.completions.create(
  model="gpt-3.5-turbo-1106",
  response_format={ "type": "json_object" },
  
  
  messages=[
    {"role": "system", "content": system_message},
    {"role": "user", "content": user_message}
  ],
  top_p=0.3 # TODO: need finetuning

)

# ai's response
response = completion.choices[0].message.content
print(response)

# the new time slots to be added
start_time, end_time = response['start_time'], response['end_time']



try:
    connection = mysql.connector.connect(**db_config)
    if connection.is_connected():
        print("Connected to AWS RDS")
        
    # Create a cursor to execute SQL queries
    cursor = connection.cursor()

    use_db_query = f"USE {db}"
    cursor.execute(use_db_query)
    print(f"Using database {db}")

  # store data
    f.create(current_datetime, cursor)
    f.insert(start_time=start_time, end_time=end_time, cursor=cursor)


except mysql.connector.Error as e:
    print(f"Error connecting to AWS RDS: {e}")
finally:
    if connection.is_connected():
        cursor.close()
        connection.close()
        print("Connection to AWS RDS closed")
