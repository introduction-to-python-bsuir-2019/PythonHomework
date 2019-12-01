"""this module contain class layer for sqllite3"""

import sqlite3
import sys
from .sqlite_scripts import scripts
from src.components.helper import Map


class Sqlite:
    """This class provided layer over sqllite3 for standard crud operation
    and help store cache into database"""

    def __init__(self, path: str) -> None:
        """
        This constructor start open connection to sqllite database
        :param path: str
        """
        self.conn = None
        self.cursor = None

        self.open(path)

    def open(self, path: str) -> None:
        """
        This method try to open sqlite connection and set current connection cursor
        Otherwise raised exceptions
        :param path: str
        :return: None
        """

        try:
            self.conn = sqlite3.connect(path,  isolation_level=None)
            self.conn.row_factory = sqlite3.Row
            self.cursor = self.conn.cursor()

        except sqlite3.Error as e:
            sys.exit(e)

    def close(self) -> None:
        """
        This method commit changes and close connection
        :return: None
        """
        if self.conn:
            self.conn.commit()
            self.cursor.close()
            self.conn.close()

    @classmethod
    def map_data(self, data: dict) -> list:
        """
        This method wrap retrieving data to Map object for proper usage
        :param data: dict
        :return: list
        """
        if isinstance(data, sqlite3.Cursor):
            return [Map(row) for row in data.fetchall()]

        return [Map(row) for row in data]


    @classmethod
    def create_database(self, path: str) -> None:
        """
        This method create cache storage database from sqllite_scripts
        Otherwise raised exceptions
        :param path: str
        :return: None
        """
        try:
            self.conn = sqlite3.connect(path,  isolation_level=None)
            self.conn.row_factory = sqlite3.Row
            cursor = self.conn.cursor()

            cursor.executescript(scripts.create_db_tables['feeds'])
            cursor.executescript(scripts.create_db_tables['feeds_entries'])
            cursor.executescript(scripts.create_db_tables['feed_entry_links'])
            cursor.executescript(scripts.create_db_tables['feed_entry_media'])

            cursor.close()

        except sqlite3.Error as e:
            sys.exit(e)

    def get(self, table: str, columns: str, limit: int=100) -> list:
        """
        This method retrieve data from specific table
        :param table: str
        :param columns: str
        :param limit: int
        :return: list
        """
        query = scripts.get.format(columns, table, limit)
        self.cursor.execute(query)

        return self.cursor.fetchall()

    def get_last(self, table: str, columns: str):
        """
        This method retrieve last entry from specific table
        :param table: str
        :param columns: str
        :return:
        """
        return self.get(table, columns, limit=1)[0]

    def where(self, table: str, *where: list, limit: int=100) -> list:
        """
        This method retrieve data with specific where statements
        :param table: str
        :param where: list
        :param limit: int
        :return: list
        """

        where = ' AND '.join('{} {} "{}" '.format(item[0], item[1], item[2]) for item in where)

        query = scripts.where.format(table, where, limit)

        self.cursor.execute(query)

        return self.cursor.fetchall()

    def find_where(self, table: str, column: str, value, type: str='=') -> int:
        """
        This method retrieve id from single entry found by specific statement
        :param table: str
        :param column: str
        :param value: Union[int, str]
        :param type: str
        :return: int
        """

        query = scripts.find_where.format(table, column, type, value)

        self.cursor.execute(query)
        row = self.cursor.fetchone()

        return row[0] if row is not None else False

    def write(self, table: str, columns: list, data: list) -> None:
        """
        This method write provided data
        :param table: str
        :param columns: list
        :param data: list
        :return: None
        """

        query = scripts.write.format(
            table, ', '.join(column for column in columns) , ', '.join( "'" + str(item) + "'" for item in data)
        )

        self.cursor.execute(query)

    def query(self, sql: str, *args):
        """
        This method provide wrap on query for further methods usage
        :param sql: str
        :param args: *
        :return:
        """
        self.cursor = self.conn.cursor()

        return self.cursor.execute(sql, args)

    def __exit__(self, exc_type, exc_value, traceback):
        """ Close connection on exit"""
        self.close()
