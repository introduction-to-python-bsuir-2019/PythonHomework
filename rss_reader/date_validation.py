from datetime import datetime

def is_valid_date(date, pattern):
    try:
        datetime.strptime(date, pattern)
        return True
    except ValueError:
        return False