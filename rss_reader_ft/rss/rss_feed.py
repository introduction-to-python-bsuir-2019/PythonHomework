import feedparser
import logging as log
from bs4 import BeautifulSoup

from conversion.json_converter import JsonConverter


class RSSFeed:
    def __init__(self, dict_args):
        self.rss_url: str = dict_args['source']
        self.limit: int = dict_args['limit']
        self.news = []
        self.rss_feed_dict = {}
        log.info('Init RSSFeed')

    def receiving_rss_data(self):
        log.info('Connect to Yahoo')
        try:
            self.rss_feed = feedparser.parse(self.rss_url)
            if self.rss_feed.bozo != 0:
                raise ConnectionError("Incorrect url")
        except Exception as ex:
            log.error('Error connection', exc_info=False)
        log.info(f'The receiving_rss_data method worked')

    def rss_data_processing(self):
        fix_quot = r"'"
        self.rss_feed_dict.update({"Feed": self.rss_feed.feed.title,
                                   "Url": self.rss_url})
        for entry in self.rss_feed.entries:
            soup = BeautifulSoup(entry.summary, features="html.parser")
            self.news.append(
                {"Title": str(entry.title).replace("&#39;", fix_quot), "Date": entry.published, "Link": entry.link,
                 "Description": soup.text, "Links": {"Source_link": entry.links[0]["href"],
                                                     "Img_links": [link.get("src") for link in soup.find_all("img") if link.get("src")]}})
        if self.limit is not None:
            self.news = self.news[:self.limit]

        self.rss_feed_dict.update({"News": self.news})
        log.info(f'The rss_data_processing method worked')

    def print_rss(self):
        print(f'Feed: {self.rss_feed_dict["Feed"]}')
        for entry in self.news:
            print(f'\nTitle: {entry["Title"]}')
            print(f'Date: {entry["Date"]}')
            print(f'Link: {entry["Link"]}\n')
            print(f'{entry["Description"]}\n')
            print(f'Links:\n[1] {entry["Links"]["Source_link"]} (link)')
            for img_link in enumerate(entry["Links"]["Img_links"]):
                print(f'[{img_link[0]+2}] {img_link[1]} (image)')
        log.info(f'The print_rss method worked')

    def convert_rss_to_json(self):
        JsonConverter(self.rss_feed_dict).convert_rss_to_format()
        log.info(f'The convert_rss_to_json method worked')

    @staticmethod
    def print_log():
        log.info(f'The print_log method worked')
        with open("app.log", "r") as file_handler:
            for line in file_handler:
                print(line)
