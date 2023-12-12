import datetime


# returns a dictionary with keys day, month, year only; YYYY-MM-DD
def start_of_week():
    #datetime format: YYYY-MM-DD HH:MM:SS.ssssss
    current_datetime = datetime.datetime.now()
    start = current_datetime - datetime.timedelta(days=current_datetime.weekday())
    next_week_start = start + datetime.timedelta(days=7)
    date = start.date() #date format: YYYY-MM-DD
    next_week_date = next_week_start.date()

    return {'day0': date.day, 'month0': date.month, 'year0': date.year, 'day1': next_week_date.day, 'month1': next_week_date.month, 'year1': next_week_date.year}


#test
result = start_of_week()
print(result) #gives 2023-12-11

