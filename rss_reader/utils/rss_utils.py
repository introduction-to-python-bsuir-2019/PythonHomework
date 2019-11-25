from datetime import datetime, date
from dateutil.parser import parse
from .exceptions import RssValueException


def get_date(date_str: str) -> date:
    """Date parser from string. If error - returns now() date"""
    try:
        news_date = parse(date_str)
    except ValueError as ex:
        news_date = datetime.now()
    return news_date


def parse_date_from_console(news_date: str) -> date:
    """Checking input date format and return date object"""

    # Check if the news_date with correct format:
    try:
        news_date = datetime.strptime(news_date, '%Y%m%d')
        news_date = news_date.strftime('%Y%m%d')
    except ValueError:
        raise RssValueException('Incorrect date format. Use %Y%m%d format (ex: 20191120)!')
    return news_date


def dict_factory(cursor, row):
    """Some magic func to retrieve raws from DB into dict"""
    dic = {}
    for idx, col in enumerate(cursor.description):
        dic[col[0]] = row[idx]
    return dic
