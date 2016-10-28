# Return true if YYYY-MM-DD is in correct format. Return false if not
def valid_date(datetime):
    datetime = datetime.split(' ')

    if len(datetime) != 2:
        print "Must be formatted as YYYY-MM-DD HH:MM:SS. Try again"
        return False
    date = datetime[0]
    time = datetime[1]

    date = date.split('-')
    if len(date) != 3:
        print "Invalid format. Date half must be formatted as YYYY-MM-DD. Try again"
        return False

    if len(date[0]) != 4 or len(date[1]) != 2 or len(date[2]) != 2:
        print "Invalid format. Try again"
        return False

    year = date[0]
    month = date[1]
    day = date[2]

    try:
        year = int(year)
        month = int(month)
        day = int(day)
    except:
        print "Y, M, and D must by integers. Try again."
        return False

    if month < 1 or month > 12:
        print "Month parameter out of range. Try again."
        return False

    if day < 1:
        print "Day parameter must be > 1. Try again."
        return False

    if month in (1, 3, 5, 7, 8, 10, 12) and day > 31:
        print "Day cannot be > 31 for that month. Try again."
        return False

    if month in (4, 6, 9, 11) and day > 30:
        print "Day parameter cannot be > 30 for that month. Try again."
        return False

    if (year % 4) == 0 and day > 29:
        print "It's a leap year. Day parameter cannot be > 29. Try again."
        return False

    if (year % 4) != 0 and day > 28:
        print "It's a leap year. Day parameter cannot be > 28. Try again."
        return False

    time = time.split(':')

    if len(time) != 3:
        print "Time must be formatted as HH:SS:MM. Try again"
        return False

    hour = time[0]
    minute = time[1]
    second = time[2]

    if len(hour) != 2 or len(minute) != 2 or len(second) != 2:
        print "Each paremeter in time must be 2 digits long. Try again."
        return False

    try:
        hour = int(hour)
        minute = int(minute)
        second = int(second)
    except:
        print "All time paremeters must be numbers. Try again."
        return False

    if hour < 0 or hour >= 24:
        print hour
        print "Hour parameter out of range. Try again."
        return False

    if minute < 0 or minute >= 60:
        print "Minute parameter out of range. Try again."
        return False

    if second < 0 or second >= 60:
        print "Second parameter out of range. Try again."
        return False