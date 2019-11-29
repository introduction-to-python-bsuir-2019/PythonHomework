import sqlite3
from os.path import exists
import sys


class Database():
    """Class working with SQLite3 database"""

    def __init__(self):
        super(Database, self).__init__()
        if not exists("cache.db"):
            conn = sqlite3.connect("cache.db")
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE `feed` (`source` text unique, `name` text)
                """)
            cursor.execute("""
                CREATE TABLE "news" ( `source` text, `date` text, 
                `title` text, `link` text UNIQUE, 
                `description` text, `links` text )
                """)
            conn.commit()
            conn.close()
        self.conn = None
        self.cursor = None

    def _open(self):
        self.conn = sqlite3.connect("cache.db")
        self.cursor = self.conn.cursor()

    def _close(self):
        self.conn.close()

    def write_data(self, data, feed, url):
        """Write news to database
        Params:
        data: turple
        feed: str
        url: str
        """
        try:
            self._open()
            for news in data:
                self.cursor.execute(""" 
                    INSERT INTO news
                    VALUES (?,?,?,?,?,?) 
                    """, news)
            self.conn.commit()
            self.cursor.execute("""
                INSERT INTO feed
                VALUES (?,?)
                """, (url, feed))
            self.conn.commit()
        except sqlite3.IntegrityError:
            pass
        except sqlite3.DatabaseError:
            print("Database error")
        finally:
            self._close()

    def read_data(self, url, date):
        """Get url & date
        Return feed & data
        """
        feed, data = None, None
        try:
            self._open()
            self.cursor.execute(f"""
                SELECT name from feed WHERE source = '{url}'
                """)
            feed = self.cursor.fetchall()
            self.cursor.execute(f"""
                SELECT * from news WHERE source = '{url}' and date = '{date}'
                """)
            data = self.cursor.fetchall()
        except Exception as e:
            print("Database reading error", e)
            sys.exit()
        finally:
            self._close()
        return feed, data
