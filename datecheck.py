# Return true if YYYY-MM-DD is in correct format. Return false if not
def valid_date(date):
    date = date.split('-')
    if len(date) != 3:
        print "Invalid format. Must be formatted as YYYY-MM-DD Try again"
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

    return True