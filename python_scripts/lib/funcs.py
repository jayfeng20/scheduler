import datetime


# returns a dictionary with keys day, month, year only; YYYY-MM-DD
def start_of_week():
    #datetime format: YYYY-MM-DD HH:MM:SS.ssssss
    current_datetime = datetime.datetime.now()
    # .weekday() gets day of the week as int; Mon = 0 Sun = 6
    start = current_datetime - datetime.timedelta(days=current_datetime.weekday())
    date = start.date() #date format: YYYY-MM-DD

    return {'day': date.day, 'month': date.month, 'year': date.year}


#test
result = start_of_week()
print(result) #gives 2023-12-11

