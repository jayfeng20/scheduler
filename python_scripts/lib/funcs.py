import datetime


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
    CREATE TABLE IF NOT EXISTS {week1.month+week1.day+week1.year} (
        id INT AUTO_INCREMENT PRIMARY KEY,
        task_name VARCHAR(255) NOT NULL,
        start_time DATETIME,
        end_time DATETIME
    )
    """
    cursor.execute(create_table_query1)

    create_table_query2 = f"""
    CREATE TABLE IF NOT EXISTS {week2.month+week2.day+week2.year} (
        id INT AUTO_INCREMENT PRIMARY KEY,
        task_name VARCHAR(255) NOT NULL,
        start_time DATETIME,
        end_time DATETIME
    )
    """
    cursor.execute(create_table_query2)


# insert rows
def insert(start_time, end_time, cursor):
    week = start_of_week(start_time)
    table_name = f'{week.month+week.day+week.year}'
    insert_query = f"""
    INSERT INTO {table_name} (task_name, start_time, end_time) VALUES ({start_time}, {end_time})
"""
    cursor.execute(insert_query)


# retrieve data

print(start_of_week())