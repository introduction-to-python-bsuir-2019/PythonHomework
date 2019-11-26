import html
import re
import json
import logging
from .cache import Cache


class News:
    """This class contains news and methods of work whit news"""
    http_header = 'http'
    img_description = 'image / ?'
    def __init__(self, feeds_dict, limit):

        logger = logging.getLogger('rss_reader')
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler = logging.FileHandler('rss_reader_logs.log')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        logger.setLevel(logging.INFO)
        self.news = dict()
        self.all_news = list()

        self.name_of_source = feeds_dict.feed['title']

        real_limit = len(feeds_dict.entries)
        if limit > 0:
            if limit < len(feeds_dict.entries):
                real_limit = limit

        cursor = Cache.get_cursor()

        for i in range(real_limit):
            list_to_cache = list()
            self.news['title'] = html.unescape(feeds_dict.entries[i].title)
            self.news['date'] = html.unescape(feeds_dict.entries[i].published)
            self.news['link'] = html.unescape(feeds_dict.entries[i].link)
            self.news['description'] = self.clean_from_tags(html.unescape(feeds_dict.entries[i].description))

            list_to_cache.append(self.news['title'])
            date_dict = feeds_dict.entries[i].published_parsed
            date_str = str(date_dict.tm_year) + str(date_dict.tm_mon) + str(date_dict.tm_mday)
            list_to_cache.append(date_str)
            list_to_cache.append(self.news['date'])
            list_to_cache.append(self.news['link'])
            list_to_cache.append(self.news['description'])

            cursor.execute('''INSERT or IGNORE INTO news (title, pub_date_key, pub_date, link, description) VALUES(?,?,?,?,?)''',
                           list_to_cache)
            ids = cursor.lastrowid
            Cache.commit()
            list_to_cache.clear()
            list_to_links = list()

            if feeds_dict.entries[i].setdefault('media_content', None):
                media = list()
                if feeds_dict.entries[i].media_content:
                    for elem in feeds_dict.entries[i].media_content:
                        if elem['url'].rfind(self.http_header, 0, len(elem['url'])) > 0:
                            links = elem['url'].split(self.http_header)
                            j = 1

                            while j < len(links):
                                media.append({'url': self.http_header + links[j], 'type': self.img_description})
                                list_to_links.append(self.http_header + links[j])
                                list_to_links.append(ids)
                                cursor.execute('''INSERT or IGNORE INTO media (link, news) VALUES(?,?)''',
                                               list_to_links)
                                list_to_links.clear()
                                j = j + 1
                                Cache.commit()
                        else:
                            media.append({'url': elem.setdefault('url', None), 'type': elem.setdefault('type', None)})
                            list_to_links.append(elem.setdefault('url', None))
                            list_to_links.append(ids)
                            cursor.execute('''INSERT or IGNORE INTO media (link, news) VALUES(?,?)''', list_to_links)
                            list_to_links.clear()
                            Cache.commit()
                self.news['media'] = media.copy()
            else:
                self.news['media'] = ''
            links = list()
            if feeds_dict.entries[i].links:
                for elem in feeds_dict.entries[i].links:
                    links.append({'url': elem.setdefault('url', None), 'type': elem.setdefault('type', None)})
                    list_to_links.append(elem.setdefault('url', None))
                    list_to_links.append(ids)
                    cursor.execute('''INSERT or IGNORE INTO links (link, news) VALUES(?,?)''', list_to_links)
                    list_to_links.clear()
            self.news['links'] = links.copy()
            self.all_news.append(self.news.copy())
        Cache.commit()
        Cache.close()

    @staticmethod
    def clean_from_tags(text_with_tags):
        """This function delete tags from string"""
        return re.sub('<.*?>', '', text_with_tags)

    def print(self):
        """This function print news to stdout in readable format"""
        print(f'Source: {self.name_of_source}\n')
        for elem in self.all_news:
            print('Title: ', elem['title'])
            print('Date: ', elem['date'])
            print('Link: ', elem['link'])
            print(f"Description: {elem['description']}\n")

            j = 1
            print('Links: ')
            for link in elem['links']:
                print(f'[{j}] {link["url"]} ({link["type"]})')
                j = j + 1

            if elem.setdefault('media', None):
                print("Media: ")
                for media in elem['media']:
                    print(f'[{j}] {media["url"]} ({media["type"]})')
                    j = j + 1
            print('\n')

    def to_json(self):
        """This function returns JSON-string with news"""
        return json.dumps({'Source:': self.name_of_source, 'Feeds': self.all_news}, ensure_ascii=False).encode('utf8')
