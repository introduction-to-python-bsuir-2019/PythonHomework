import sqlite3


class Database():
    """docstring for Database"""

    def __init__(self):
        super(ClassName, self).__init__()
        self.conn = None
        self.cursor = None
        

    def _open(self):
        self.conn = sqllite3.connect("cache.db")
        self.cursor = conn.cursore()

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
