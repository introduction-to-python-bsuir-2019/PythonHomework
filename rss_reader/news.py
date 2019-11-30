import html
import os
import re
import json
import logging
from .cache import Cache
import base64
import requests


class News:
    """This class contains news and methods of work whit news"""

    http_header = 'http'
    err_media_type = 'No type'

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

            date_dict = feeds_dict.entries[i].published_parsed
            date_str = str(date_dict.tm_year) + str(date_dict.tm_mon) + str(date_dict.tm_mday)

            list_to_cache.append(self.news['title'])
            list_to_cache.append(date_str)
            list_to_cache.append(self.news['date'])
            list_to_cache.append(self.news['link'])
            list_to_cache.append(self.news['description'])

            self.news['media'] = self._parse_media(feeds_dict.entries[i])
            self.news['links'] = self._parse_links(feeds_dict.entries[i])

            self._cache_feed(list_to_cache, self.news['links'], self.news['media'], cursor)

            self.all_news.append(self.news.copy())
        Cache.close()

    def _parse_links(self, news_dict):
        """This function parse links of feed"""
        list_of_links = list()
        if news_dict.links:
            for elem in news_dict.links:
                list_of_links.append({'url': elem.setdefault('url', None), 'type': elem.setdefault('type', None)})
        return list_of_links

    def _parse_media(self, news_dict):
        """This function parse media of feed"""
        if news_dict.setdefault('media_content', None):
            media = list()
            if news_dict.media_content:
                for elem in news_dict.media_content:
                    if elem['url'].rfind(self.http_header, 0, len(elem['url'])) > 0:
                        # Some sources of news write two links in one string of media. And only second string is image
                        links = elem['url'].split(self.http_header)
                        media.append({'url': self.http_header + links[2], 'type': "img"})
                    else:
                        if elem.setdefault('url', None):
                            media.append({'url': elem.setdefault('url', None),
                                          'type': elem.setdefault('type', None)})
            return media
        else:
            return ''

    def _cache_feed(self, list_of_main_info, list_of_links, list_of_media, cursor):
        """This function write feed to cache"""
        cursor.execute('''INSERT or IGNORE INTO news (title, pub_date_key, pub_date, link, description)
                     VALUES(?,?,?,?,?)''', list_of_main_info)
        ids = cursor.lastrowid

        list_to_cache_of_links = list()
        for elem in list_of_links:
            list_to_cache_of_links.append(elem.setdefault('url', None))
            list_to_cache_of_links.append(ids)
            cursor.execute('''INSERT or IGNORE INTO links (link, news) VALUES(?,?)''', list_to_cache_of_links)
            list_to_cache_of_links.clear()

        list_to_cache_of_media = list()
        for elem in list_of_media:
            list_to_cache_of_media.append(elem.setdefault('url', None))
            list_to_cache_of_media.append(ids)
            cursor.execute('''INSERT or IGNORE INTO media (link, news) VALUES(?,?)''', list_to_cache_of_media)
            list_to_cache_of_media.clear()

        Cache.commit()

    @staticmethod
    def clean_from_tags(text_with_tags):
        """This function delete tags from string"""
        return re.sub('<.*?>', '', text_with_tags)

    def print(self):
        """This function print news to stdout in readable format"""
        print(f'Source: {self.name_of_source}\n')
        for elem in self.all_news:
            print(f'Title: {elem["title"]}')
            print(f'Date: {elem["date"]}')
            print(f'Link: {elem["link"]}')
            print(f'Description: {elem["description"]}\n')

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

    def to_json(self):
        """This function returns JSON-string with news"""
        return json.dumps({'Source:': self.name_of_source, 'Feeds': self.all_news}, ensure_ascii=False).encode('utf8')

    def to_fb2(self, filepath):
        if filepath[-4::] != ".fb2":
            filename = filepath + ".fb2"
        with open(filename, 'w', encoding="utf-8") as fb2_file:
            fb2_file.write('<?xml version="1.0" ?>\n')
            fb2_file.write(f'''<FictionBook xmlns:l="http://www.w3.org/1999/xlink"><description/><body>''')
            fb2_file.write(f'''<title><p>{self.name_of_source.replace("&", "&amp;")}</p></title><empty-line/>''')
            for elem in self.all_news:
                fb2_file.write(f'<section><title><p>{elem["title"].replace("&", "&amp;")}</p></title>')
                fb2_file.write(f'<p>Date of posting: {elem["date"].replace("&", "&amp;")}</p>')
                fb2_file.write(f'<p>{elem["description"].replace("&", "&amp;")}</p><empty-line/>')
                fb2_file.write(f'<p>Source: {elem["link"]}</p></section>'.replace("&", "&amp;"))

                for media in elem['media']:
                    if media['type'] != self.err_media_type:
                        fb2_file.write(f'''<empty-line/><empty-line/>
                        <image l:href="#{media["url"]}"/><empty-line/><empty-line/>''')
                        pass
            fb2_file.write('</body>')
            for elem in self.all_news:
                for media in elem['media']:
                    if media['type'] != self.err_media_type:
                        fb2_file.write(f'<binary content-type="image/png" id="{media["url"]}">')
                        content = base64.b64encode(requests.get(media["url"]).content)
                        fb2_file.write(content.decode('ascii'))
                        fb2_file.write('</binary>')
            fb2_file.write('</FictionBook>')

        print(f'All news you can find at {os.path.realpath(filename)}')

    def to_html(self, filepath):
        if filepath[-5::] != ".html":
            filename = filepath + ".html"
        with open(filename, 'w', encoding="utf-8") as html_file:
            html_file.write(f'<html>\n<head>{self.name_of_source}</head>\n<body>\n')
            for elem in self.all_news:
                html_file.write(f'<h3>{elem["title"]}</h3>')
                html_file.write(f'<p>Date of posting: {elem["date"]}</p>')
                html_file.write(f'<p>{elem["description"]}</p>')
                html_file.write(f'<p><a href="{elem["link"]}">Link to source</a></p>')

                for media in elem['media']:
                    if media['type'] != self.err_media_type:
                        html_file.write(f'<p><img src="{media["url"]}"></p>')
                html_file.write('<hr>')
            html_file.write('</body></html>')
        print(f'All news you can find at {os.path.realpath(filename)}')
