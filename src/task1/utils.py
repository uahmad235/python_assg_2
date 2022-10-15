from datetime import datetime, date, time 


def calculate_today_stamp():
    # the start of the current day
    return datetime.combine(date.today(), time())

def convert_time(hour_from, minute_from, hour_to, minute_to):
 
    today_date = calculate_today_stamp()
    time_from = datetime.now().replace(hour = hour_from, minute = minute_from, second = 0, microsecond = 0)
    time_to = datetime.now().replace(hour = hour_to, minute = minute_to, second = 0, microsecond = 0)

    return time_from, time_to