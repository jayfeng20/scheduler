import datetime


# returns a dictionary with keys day, month, year only
def start_of_week():
    #datetime format: YYY-MM-DD HH:MM:SS.ssssss
    current_datetime = datetime.datetime.now()
    # .weekday() gets day of the week as int; Mon = 0 Sun = 6
    start = current_datetime - datetime.timedelta(days=current_datetime.weekday())
    #.date() extracts the date part (w/o time info)
    return start.date()


#tests
result = start_of_week()
print("Start of this week" + result)