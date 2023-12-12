import datetime
from datetime import timedelta
import mysql.connector

# returns 2 datetime objects
def start_of_week(current_datetime=datetime.datetime.now()):
    start = current_datetime - datetime.timedelta(days=current_datetime.weekday())
    
    # Set the time to 12:00 AM (midnight)
    start = start.replace(hour=0, minute=0, second=0, microsecond=0)
    
    if start.weekday() != 0:
        start -= datetime.timedelta(days=1)  # Move back to Monday

    next_week_start = start + datetime.timedelta(days=7)
    
    return start, next_week_start



# create table
def create(week, cursor):
    week1, week2 = start_of_week()
    create_table_query1 = f"""
    CREATE TABLE IF NOT EXISTS t{str(week1.month)+str(week1.day)+str(week1.year)} (
        id INT AUTO_INCREMENT PRIMARY KEY,
        task_name VARCHAR(255) NOT NULL,
        start_time DATETIME,
        end_time DATETIME
    )
    """
    cursor.execute(create_table_query1)

    create_table_query2 = f"""
    CREATE TABLE IF NOT EXISTS t{str(week2.month)+str(week2.day)+str(week2.year)} (
        id INT AUTO_INCREMENT PRIMARY KEY,
        task_name VARCHAR(255) NOT NULL,
        start_time DATETIME,
        end_time DATETIME
    )
    """
    cursor.execute(create_table_query2)


# insert rows
def insert(task_name, start_times, end_times, cursor):
    for i in range(len(start_times)):
        start_time = start_times[i]
        end_time = end_times[i]
        week1, week2 = start_of_week(start_time)
        table_name = f'{str(week1.month)+str(week1.day)+str(week1.year)}'
        # print(table_name, start_time, end_time)
        insert_query = f"""
        INSERT INTO t{table_name} (task_name, start_time, end_time) VALUES ('{task_name}', '{start_time}', '{end_time}');
    """
        # print(insert_query)
        cursor.execute(insert_query)
        commit_query = """COMMIT;"""
        cursor.execute(commit_query)


# retrieve data for this week and next week
def retrieve(current, cursor):
    week1, week2 = start_of_week(current_datetime=current)
    table1 = f'{str(week1.month)+str(week1.day)+str(week1.year)}'
    select_query1 = f"""
    SELECT * FROM t{table1}
"""
    cursor.execute(select_query1)
    rows1 = cursor.fetchall()

    table2 = f'{str(week2.month)+str(week2.day)+str(week2.year)}'
    select_query2 = f"""
    SELECT * FROM t{table2}
"""
    cursor.execute(select_query2)
    rows2 = cursor.fetchall()
    return rows1, rows2

#converting chatgpt data into week
#dt = python datetime object 
# the console isn't giving me any errors does it look ok on ur end
# it only gives one week matrix, we need two weeks so wouldn't this return a 7 col x 16 rows
# im confued
# this returns exactly what we need for 
#week, we need two of these but in a 3d matri 
# so 2 x 8 x 7 matrix

# also we should have the dt1 and dt2 be the same day, so we use what day it currently is to figure out which week the 
# time slot goes into

# for ecxample today is the 12th so that would be Week 1, Tuesday so if there is a slot that is 12th it will be week 1,
# but if its 12/19 it will be in week 2

# Jonathan says: datetime.datetime.now() is the current date and time, we only care about the date

# also we need to combine these once we get them so we should make a method to combine calendar matrices

def create_calendar(dt1, dt2):
    #initialize 3d matrix 7 days per week, 8 hrs/day
    cal = [[[0 for _ in range(7)] for _ in range(8)] for _ in range(2)]
    diff = dt2 - dt1 
    for i in range(diff.days + 1):
        day = timedelta(days=i) + dt1 
        row = day.day // 7
        week = 0 if row < 8 else 1
        column = day.weekday()

        cal[week][row][column] = 1
        # if day.weekday() < dt1.weekday(): 
        #     week = 0
        # else:
        #     week = 1
        # day_of_week = day.weekday() 
        # hour = day.hour

        # cal[week][day_of_week][hour] = 1

    return cal 

# if __name__ == "__main__":
#     #testing create_cal 
#     dt1 = datetime.date(2023, 12, 1)
#     dt2 = datetime.date(2023, 12, 1) 
#     print (create_calendar(dt1, dt2))