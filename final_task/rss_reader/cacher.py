"""
this module provides tools for caching cache_news

it includes functions for work with database and support ones
"""

import sqlite3
from re import match

def init_database():
    """
    this function creates and initizlizes database for caching news
    """
    connection_obj = sqlite3.connect('cache.db')
    cursor_obj = connection_obj.cursor()
    cursor_obj.execute(
        '''CREATE TABLE IF NOT EXISTS cache (id integer primary key, feed text, title text, pub_date text, pub_parsed text, link text, description text, hrefs text)'''
    )
    connection_obj.commit()

    return connection_obj, cursor_obj

def cache_news(connection_obj, cursor_obj, news):
    """
    this function adds parsed news in database
    """
    for post in news:
        cursor_obj.execute(
            '''INSERT INTO cache (feed, title, pub_date, pub_parsed, link, description, hrefs) VALUES (?, ?, ?, ?, ?, ?, ?)''',
            (post['feed'], post['title'], post['pub_date'], post['pub_parsed'], post['link'], post['description'], hrefs_to_text(post['hrefs']))
        )
    connection_obj.commit()

    return

def get_cached_news(cursor_obj, date):
    """
    this function fetches news from database and return them as a list
    """
    cursor_obj.execute('''SELECT * FROM cache WHERE pub_parsed=?''', (date, ))
    rows = cursor_obj.fetchall()

    news = []
    for row in rows:
        data = {}
        data['feed'] = row[1]
        data['title'] = row[2]
        data['pub_date'] = row[3]
        data['pub_parsed'] = row[4]
        data['link'] = row[5]
        data['description'] = row[6]

        hrefs = row[7].split("--|--")
        try:
            data['hrefs'] = [tuple(item.split("-|-")) for item in hrefs[0].split("-+-") if item != '']
            data['hrefs'] += [tuple(item.split("-|-")) for item in hrefs[1].split("-+-") if item != '']
        except IndexError:
            pass
        news.append(data)

    return news

def hrefs_to_text(link_list):
    """
    this function represents the list of links connected to post to text form
    """
    res_line = ''
    ind = -1
    for tpl in link_list:
        if tpl[1] != 'image':
            res_line += f"-+-{tpl[0]}-|-{tpl[1]}"
        else:
            res_line += '--|--'
            ind = link_list.index(tpl)
            break

    if ind != -1:
        for tpl in link_list[ind:]:
            res_line += f"{tpl[0]}-|-{tpl[1]}-|-{tpl[2]}-+-"

    return res_line

def is_valid_date(line):
    """
    this function checks a date parameter for suiting date format
    """
    date = r"^[1-2][0-9]{3}[0-1][0-9][0-3][0-9]$"
    return match(date, line)
