import sqlite3
import sys
from .sqlite_scripts import scripts
from src.components.helper import Map


class Sqlite:
    def __init__(self, path):

        self.conn = None
        self.cursor = None

        self.open(path)

    def open(self, path: str) -> None:

        try:
            self.conn = sqlite3.connect(path,  isolation_level=None)
            self.conn.row_factory = sqlite3.Row
            self.cursor = self.conn.cursor()

        except sqlite3.Error as e:
            sys.exit(e)

    def close(self):

        if self.conn:
            self.conn.commit()
            self.cursor.close()
            self.conn.close()

    def map_data(self, data):
        if isinstance(data, sqlite3.Cursor):
            return [Map(row) for row in data.fetchall()]

        return [Map(row) for row in data]


    @classmethod
    def create_database(self, path: str) -> str:
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

    def get(self, table, columns, limit=100):

        query = scripts.get.format(columns, table, limit)
        self.cursor.execute(query)

        return self.cursor.fetchall()

    def get_last(self, table, columns):
        return self.get(table, columns, limit=1)[0]

    def where(self, table: str, *where: list, limit: int=100):

        where = ' AND '.join('{} {} "{}" '.format(item[0], item[1], item[2]) for item in where)

        query = scripts.where.format(table, where, limit)

        self.cursor.execute(query)

        return self.cursor.fetchall()

    def find_where(self, table, column, value, type='='):

        query = scripts.find_where.format(table, column, type, value)

        self.cursor.execute(query)
        row = self.cursor.fetchone()

        return row[0] if row is not None else False

    def write(self, table, columns, data):

        query = scripts.write.format(
            table, ', '.join(column for column in columns) , ', '.join( "'" + str(item) + "'" for item in data)
        )

        self.cursor.execute(query)

    def query(self, sql, *args):
        self.cursor = self.conn.cursor()

        return self.cursor.execute(sql, args)

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()
