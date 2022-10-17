from datetime import datetime, date, time 


def calculate_today_stamp():
    """
	  Function that return the very start of the current date
	  Example: 2022-10-17 00:00:00
    """
    return datetime.combine(date.today(), time())

def convert_time(hour_from, minute_from, hour_to, minute_to):
  """
	Function to convert user input time into datetime object
	Parameters:
		  hour_from: [Integer] hour of starting
      minute_from: [Integer] minute of starting
      hour_to:   [Integer] hour of ending
      minute_to:   [Integer] minute of ending
    Return two objects: Time from and Time to
  """
  today_date = calculate_today_stamp()
  time_from = datetime.now().replace(hour = hour_from, minute = minute_from, second = 0, microsecond = 0)
  time_to = datetime.now().replace(hour = hour_to, minute = minute_to, second = 0, microsecond = 0)

  return time_from, time_to