"""Module, which allows to cache news while program is called."""

import logging
import sqlite3

from .rss_reader_consts import *


ROOT_LOGGER_NAME = 'RssReader'
MODULE_LOGGER_NAME = ROOT_LOGGER_NAME + '.caching_news'


DB_NAME = 'news.db'

HEADER_TABLE_NAME = 'date_'


def _convert_date_to_YYYYMMDD(date: str) -> str:
    """Convert date, which got by feedparser from xml-format to YYYYMMDD."""
    return (''.join(date.split()[3:0:-1])).replace(date.split()[2], MONTHS[date.split()[2]])


class DataBaseConn:
    """Context Manager, which work with sqlite3."""

    def __init__(self, db_name: str):
        """Initialize name of database."""
        self._db_name = db_name

    def __enter__(self):
        self._conn = sqlite3.connect(self._db_name)
        return self._conn

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._conn.commit()
        self._conn.close()
        if exc_val:
            raise


def table_create(table_name: str) -> None:
    """Create table on datebase."""
    command = '''CREATE TABLE if not exists
                            {}
                            (
                            title text,
                            date_ text,
                            link text,
                            img_link text,
                            short_content text
                            )
                            '''.format(table_name)

    with DataBaseConn(DB_NAME) as connection:
        cursor = connection.cursor()
        cursor.execute(command)


def db_write(date: str, title: str, link: str, img_link: str, short_content: str) -> None:
    """Write item in datebase."""
    YYYYMMDD_date = _convert_date_to_YYYYMMDD(date)

    table_create(HEADER_TABLE_NAME + YYYYMMDD_date)

    with DataBaseConn(DB_NAME) as connection:
        cursor = connection.cursor()
        cursor.execute("INSERT INTO {} VALUES (?,?,?,?,?)"
                       .format(HEADER_TABLE_NAME + YYYYMMDD_date),
                              (title, date, link, img_link, short_content))


def get_list_of_tables() -> str:
    """Get list of tables (dates)."""
    with DataBaseConn(DB_NAME) as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM sqlite_master where type='table'")

        tables = cursor.fetchall()

    tables_names = ''
    for table in tables:
        tables_names += '\n' + table[2][5:]

    return tables_names


def db_read(date: str) -> str:
    """Read items from table with name: date of datebase."""
    with DataBaseConn(DB_NAME) as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT DISTINCT * FROM {}".format(HEADER_TABLE_NAME + date))

        rows = cursor.fetchall()
        news = ''
        for row in rows:
            news += KEYWORD_TITLE + row[0] + EN
            news += KEYWORD_DATE + row[1] + EN
            news += KEYWORD_LINK + row[2] + EN
            news += KEYWORD_IMG_LINK + row[3] + EN
            news += KEYWORD_CONTENT + row[4] + EN
            news += NEWS_SEPARATOR + DEN

    return news
