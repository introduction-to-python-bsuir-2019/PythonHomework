from datetime import datetime, date
from dateutil.parser import parse


def get_date(date: str) -> date:
    try:
        news_date = parse(date)
    except ValueError as ex:
        news_date = datetime.now()
    return news_date
