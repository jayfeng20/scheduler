import datetime
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
    CREATE TABLE IF NOT EXISTS t{week1.month+week1.day+week1.year} (
        id INT AUTO_INCREMENT PRIMARY KEY,
        task_name VARCHAR(255) NOT NULL,
        start_time DATETIME,
        end_time DATETIME
    )
    """
    cursor.execute(create_table_query1)

    create_table_query2 = f"""
    CREATE TABLE IF NOT EXISTS t{week2.month+week2.day+week2.year} (
        id INT AUTO_INCREMENT PRIMARY KEY,
        task_name VARCHAR(255) NOT NULL,
        start_time DATETIME,
        end_time DATETIME
    )
    """
    cursor.execute(create_table_query2)


# insert rows
def insert(task_name, start_time, end_time, cursor):
    week1, week2 = start_of_week(start_time)
    print(week1)
    table_name = f'{week1.month+week1.day+week1.year}'
    
    insert_query = f"""
    INSERT INTO t{table_name} (task_name, start_time, end_time) VALUES ('{task_name}', '{start_time}', '{end_time}')
"""
    print(insert_query)
    cursor.execute(insert_query)


# retrieve data for this week and next week
def retrieve(current, cursor):
    week1, week2 = start_of_week(current_datetime=current)
    table1 = f'{week1.month+week1.day+week1.year}'
    select_query1 = f"""
    SELECT * FROM t{table1}
"""
    cursor.execute(select_query1)
    rows1 = cursor.fetchall()

    table2 = f'{week2.month+week2.day+week2.year}'
    select_query2 = f"""
    SELECT * FROM t{table2}
"""
    cursor.execute(select_query2)
    rows2 = cursor.fetchall()
    return rows1, rows2
