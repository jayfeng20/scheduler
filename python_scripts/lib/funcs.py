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
def create_calendar(dt1, dt2):
    #initialize 3d matrix 7 days per week, 8 hrs/day
    cal = [[[0 for _ in range(7)] for _ in range(8)] for _ in range(2)]
    
    w1, w2 = start_of_week()
    week = w1 if dt1 < w2 else w2
    weekIndex = 0 if dt1 < w2 else 1
    dayIndex = dt1.day - week.day
    startIndex = dt1.hour - 9
    endIndex = dt2.hour - 9

    for i in range(startIndex, endIndex):
        cal[weekIndex][i][dayIndex] = 1

    return cal 

if __name__ == "__main__":
    #testing create_cal 
    dt1 = datetime.datetime(2023, 12, 12, 15)
    dt2 = datetime.datetime(2023, 12, 12, 17)
    
    output = [[
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0, 0],
    ], [
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
    ]]

    print(create_calendar(dt1, dt2) == output)