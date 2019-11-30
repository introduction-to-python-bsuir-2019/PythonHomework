import sqlite3
import sys
from .sqlite_scripts import scripts


class Sqlite:
    def __init__(self, path):

        self.conn = None
        self.cursor = None

        self.open(path)

    def open(self, path: str) -> None:

        try:
            self.conn = sqlite3.connect(path,  isolation_level=None)
            self.cursor = self.conn.cursor()

        except sqlite3.Error as e:
            sys.exit(e)

    def close(self):

        if self.conn:
            self.conn.commit()
            self.cursor.close()
            self.conn.close()

    @classmethod
    def create_database(self, path: str) -> str:
        try:
            self.conn = sqlite3.connect(path,  isolation_level=None)
            cursor = self.conn.cursor()

            cursor.executescript(scripts['create_db_tables']['feeds'])
            cursor.executescript(scripts['create_db_tables']['feeds_entries'])

            cursor.close()

        except sqlite3.Error as e:
            sys.exit(e)

    def get(self, table, columns, limit=None):

        query = scripts.get('get').format(columns, table)
        self.cursor.execute(query)

        rows = self.cursor.fetchall()

        return rows[len(rows) - limit if limit else 0:]

    def findWhere(self, table, column, value, type='='):

        query = scripts.get('find_where').format(table, column, type,value)

        self.cursor.execute(query)
        row = self.cursor.fetchone()

        return row[0] if row is not None else False

    def getLast(self, table, columns):

        return self.get(table, columns, limit=1)[0]

    def write(self, table, columns, data):

        query = scripts.get('write').format(
            table, ', '.join(column for column in columns) , ', '.join( "'" + str(item) + "'" for item in data)
        )

        self.cursor.execute(query)

        return self.cursor.fetchall() or False

    def query(self, sql):
        self.cursor.execute(sql)

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

