import time
from datetime import datetime

pattern = '%Y%m%d'


def get_current_date_str():
    """
    This function returns string with current date in format 'yyyymmdd'
    :return: str
    """
    current_date = datetime.today()
    return current_date.strftime(pattern)


def get_current_date_tuple():
    """
    This function return current date in tuple
    :return: struct_time
    """
    return datetime.now().utctimetuple()


def is_valid_date(date_str):
    """
    This function defines if date_str is valid date in format 'yyyymmdd'
    :param date_str: str
    :return: bool
    """
    try:
        datetime.strptime(date_str, pattern)
        return True
    except ValueError:
        return False


def get_date_str(date_tuple):
    """
    THis function converts param date_tuple to str in format 'yyyymmdd'
    :param date_tuple: struct_time
    :return: str
    """
    return time.strftime(pattern, date_tuple)
