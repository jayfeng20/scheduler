from openai import OpenAI
import os  
import calendar
import datetime
import json 
from dotenv import load_dotenv
load_dotenv()

import lib.funcs as f
import mysql.connector




def run(task_name='t3', task_type='project', task_time=4, task_due=7):
    task_name = task_name
    task_type = task_type
    expected_time = int(task_time)
    due_in = 2
    # due_in = task_due
    
    assert expected_time <= 24 and 1 <= expected_time
    assert due_in >= 1 and due_in <= 7 # due in at least 1 day and at most 1 week
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
        start_times = [row[2] for row in rows1]
        start_times.extend([row[2] for row in rows2])
        end_times = [row[3] for row in rows1]
        end_times.extend([row[3] for row in rows2])
        for i in range(len(start_times)):
            alr_booked.append(f"{start_times[i]} to {end_times[i]}")
        print(f'alr_booked: {alr_booked}')

      # TODO: Use alr_booked to display initialize the calendar

        system_message = """
        You are a smart assistant who is good at time management. 
        You will be given current time, a task, the expected hours to finish the task, how many days until the task is due and time slots that are already booked.
        You have to schedule timeslots that do not overlap with already booked timeslots.
        You are allowed to assign the tasks to up to 2 timeslots as long as the timeslots add up to the expected hours.
        You will find time slot(s) within the next 7 days, between 9am and 5pm and can be across different days to schedule this task.
        Your output is in the form of a json object with 2 fields. The first field is named "new_start_times" and 
        it contains a list of python datetime objects that represent the starting times of the time slots you scheduled.
        The second field is named "new_end_times" and 
        it contains a list of python datetime objects that represent the ending times of the time slots you scheduled.
        So the first element of the new_start_times list and the first element of the new_end_times list would form the first 
        time slot you scheduled.
        """

        user_message = "Can you please find the best time slot(s) for me to do the following task?" + \
        "I don't want to work for too long in one seating. So please break long tasks down if possible." + \
        f"""
        time right now: {current_datetime}
        expected duration: {expected_time} hours to finish, 
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
          top_p=0.1
        )

        # ai's response
        response = completion.choices[0].message.content
        response = json.loads(response)

        # the new time slots to be added
        new_start_times, new_end_times = response['new_start_times'], response['new_end_times']
        date_time_format = "%Y-%m-%dT%H:%M:%S"
        for i in range(len(new_end_times)):
            new_start_times[i] = datetime.datetime.strptime(new_start_times[i], date_time_format)
            new_end_times[i] = datetime.datetime.strptime(new_end_times[i], date_time_format)
        # print("test1", new_start_times, new_end_times)
        f.insert(task_name=task_name, start_times=new_start_times, end_times=new_end_times, cursor=cursor)
        


    except mysql.connector.Error as e:
        print(f"Error connecting to AWS RDS: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("Connection to AWS RDS closed")
        return start_times, end_times, new_start_times, new_end_times

# run()