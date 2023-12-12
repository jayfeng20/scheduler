from openai import OpenAI
import os  
import calendar
import datetime
import json 
from dotenv import load_dotenv
load_dotenv()

import lib.funcs as f
import mysql.connector




def run(task_name='t3', task_type='project', task_time=5, task_due=3):
    task_name = task_name
    task_type = task_type
    expected_time = int(task_time)
    due_in = 2
    # due_in = task_due
    
    assert expected_time <= 24 and 1 <= expected_time
    assert due_in >= 1 and due_in <= 7 # due in at least 1 day and at most 1 week
    print(task_name)
    current_datetime = datetime.datetime.now()


    # mysql config
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

    # openai config
    key = os.environ.get("OPENAI_API_KEY")
    client = OpenAI(
      api_key=key,
    )

    connection = mysql.connector.connect(**db_config)

    # start the connectionn
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

        alr_booked = []
        rows1, rows2 = f.retrieve(current=current_datetime, cursor=cursor)
        print(rows1, rows2)
        start_times = [row[2] for row in rows1]
        start_times.extend([row[2] for row in rows2])
        end_times = [row[3] for row in rows1]
        end_times.extend([row[3] for row in rows2])
        for i in range(len(start_times)):
            alr_booked.append(f"{start_times[i]} to {end_times[i]}")
        print(rows1, rows2)
        print(f'alr_booked: {alr_booked}')

      # TODO: Use alr_booked to display initialize the calendar

        system_message = """
        You are a concise and precise assistant. You find the most reasonable time slot(s) to assign this task within the next week
        and before the due date. If there's extra time, avoid meal time and sleep time.
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
        response = json.loads(response)

        # the new time slots to be added
        start_time, end_time = response['start_time'], response['end_time']
        date_time_format = "%Y-%m-%dT%H:%M:%S"
        start_time, end_time = datetime.datetime.strptime(start_time, date_time_format), datetime.datetime.strptime(end_time, date_time_format)
        f.insert(task_name=task_name, start_time=start_time, end_time=end_time, cursor=cursor)
        


    except mysql.connector.Error as e:
        print(f"Error connecting to AWS RDS: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("Connection to AWS RDS closed")
        return start_times, end_times, start_time, end_time
