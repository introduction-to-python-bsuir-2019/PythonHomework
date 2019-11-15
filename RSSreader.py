import feedparser
import json
from bs4 import BeautifulSoup


class RSSreader:
    """ Reads news from RSS url and prints them """
    def __init__(self, args):
        self.args = args

    def get_feed(self):
        """ Returns read feed """
        news_feed = feedparser.parse(self.args.get_args().url)
        return news_feed.entries[:self.args.get_args().limit]

    def print_feed(self, entries):
        """ Prints feed in stdout """
        for entry in entries:
            print('========================================================')
            print(f'Title: {entry.title}')
            print(f'Published: {entry.published}', end='\n\n')
            print(f'Summary: {BeautifulSoup(entry.summary, "html.parser").text}', end='\n\n')
            print(f'Link: {entry.link}')
            print('========================================================')

    def print_feed_json(self, entries):
        """ Prints feed in stdout in JSON format """
        for entry in entries:
            feed = {
                'Title': entry.title,
                'Published': entry.published,
                'Summary': BeautifulSoup(entry.summary, "html.parser").text,
                'Link': entry.link,
            }
            print('========================================================')
            print(json.dumps(feed, indent=2, ensure_ascii=False))
            print('========================================================')
