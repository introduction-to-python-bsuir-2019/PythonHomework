import sqlite3
from arg import args
from sqlite3 import Error
from date_converter import convert_date


def sql_connection():
    '''Get connected to the database'''
    try:
        con = sqlite3.connect('mydatabase.db')
        return con
    except Error:
        print(Error)


def sql_fetch(con):
    '''Extract info from the database'''
    console_args = args()
    cursorObj = con.cursor()
    cursorObj.execute('SELECT * FROM news')
    while True:
        row = cursorObj.fetchone()
        if row == None:
            break
        if convert_date(row[1]) == console_args.date:
            print(' Title:',row[0],'\n','Date:',row[1],'\n','Link:',row[2],'\n','Description:',row[3],'\n')