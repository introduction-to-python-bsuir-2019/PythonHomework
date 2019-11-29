import sqlite3
from os.path import exists

class Database():
    """docstring for Database"""

    def __init__(self):
        super(Database, self).__init__()
        if not exists("cache.db"):
            conn = sqlite3.connect("cache.db")
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE `feed` (`source` text unique, `name` text)
                """)
            cursor.execute("""
                CREATE TABLE news(source text, 
                date text, title text, link text, 
                description text, links text)
                """)
            conn.commit()
            conn.close()
        self.conn = None
        self.cursor = None
        

    def _open(self):
        self.conn = sqllite3.connect("cache.db")
        self.cursor = conn.cursor()

    def _close(self):
        self.conn.close()

    def write_data(self, data, feed, url):
        try:
            self._open()
            self.cursor.execute(""" 
                INSERT INTO news
                VALUES (?,?,?,?,?,?) 
                """, data)
            self.cursor.execute("""
                INSERT INTO feed
                VALUES (?,?)
                """, (url, feed))
        except sqlite3.DatabaseError as err:
            print("Database error")
        else:
            self.conn.commit()
        finally:
            self._close()

    def read_data(self, url, date):
        data = None
        return data
