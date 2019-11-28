import sqlite3

from sqlite3 import Error

def sql_connection():
    try:
        con = sqlite3.connect('mydatabase.db')
        return con
    except Error:
        print(Error)


def sql_table(con, entities):
    cursorObj = con.cursor()
    try:
        cursorObj.execute("CREATE TABLE IF NOT EXISTS news(title, published, link, description)")
    finally:
        cursorObj.execute('INSERT OR REPLACE INTO news(title, published, link, description) VALUES(?, ?, ?, ?)', entities)
    con.commit()


def sql_fetch(con):
    cursorObj = con.cursor()
    cursorObj.execute('SELECT * FROM news')
    while True:
        row = cursorObj.fetchone()
        if row == None:
            break
        print('Title:',row[0],'\n','Date:',row[1],'\n','Link:',row[2],'\n','Description:',row[3],'\n')
