"""
Python RSS reader

Designed to download news from the entered url.

Opportunities:
    * Get version
    * Conversion to JSON
    * Logging
    * Limiting articles
    * Caching news feeds in SQLite database

For information enter
    "python rss_reader.py -h"
in terminal to find more information.

"""
__package__ = 'rss-reader'

import datetime
import json
import logging
import feedparser
import argparse

from htmlparser import *
from storage_controller import *


class RSSReader:
    def __call__(self, source, limit, as_json, date):
        """
        Procedure executing program. Get additional setting parameters and running.

        :param source: URL for downloading news articles
        :param limit: limit news topics if this parameter provided
        :param as_json: show news articles as JSON
        :param date: print cached articles by date
        :type source: str
        :type limit: int
        :type as_json: bool
        :type date: str
        """
        if limit and limit < 1:
            print(f"Error: Impossible parse 0 and less RSS Feeds")
            exit(0)

        if not date:
            logging.info("Start loading articles from RSS source")
            articles = self._get_articles_from_url(source, limit)
            logging.info("Completed. Saving articles in cache")
            count = StorageController().save(source, articles['articles'], articles['title'])
            logging.info(f"Completed. {count} articles was saved in cache")
        else:
            logging.info("Start loading from cache")
            try:
                logging.info("Check date format")
                datetime.datetime.strptime(date, "%Y%m%d")
            except ValueError:
                print(f"Error format date {date}. Need '%Y%m%d'")
                exit(0)
            logging.info("Date is correct. Start loading by date")
            articles = StorageController().load(source, date, limit)

        logging.info("All articles was successfully loaded")

        if as_json:
            self.json_print(articles)
        else:
            self.sample_print(articles)

    @staticmethod
    def _get_articles_from_url(source, limit):
        logging.info("Completed. Check the availability of URL.")

        if 'status' not in (response := feedparser.parse(source.strip())) or len(response.entries) == 0:
            print(f"Error: Impossible parse RSS Feeds from url '{source}'")
            exit(0)

        logging.info("Completed. Check status code of response.")

        if response.status in range(200, 300):
            logging.info(f"Status code {response.status}. Getting articles from '{source}' was successful")
        else:
            print(f"Error connecting with URL '{source.strip()}' with status code {response.status}.")
            exit(0)

        return Parser.parse(response, limit)

    @staticmethod
    def sample_print(articles):
        """
        Procedure for sample output of news articles.

        :param articles: dict with title and list of news articles
        :type articles: dict
        """
        logging.info("Start sample output")

        if (title := articles.get('title', None)) is not None:
            print(f"Feed: {title}\n")

        for article in articles['articles']:
            print(f"Title: {article['title']}\n"
                  f"Date: {article['pubDate']}\n"
                  f"Link: {article['link']}\n\n"
                  f"{article['description']}\n\n"
                  f"Links:")
            for link in article['links']:
                print(link)
            print('################################################################################')

    @staticmethod
    def json_print(articles):
        """
        Procedure for output articles in JSON format.

        :param articles: dict with title and list of news articles
        :type articles: dict
        """
        logging.info("Converting all articles to JSON")
        data = json.dumps(articles)
        logging.info("Completed. Output JSON")
        print(data)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('source', action='store', type=str, help='RSS URL')
    parser.add_argument('--version', action='store_true', help='Print version info')
    parser.add_argument('--json', action='store_true', help='Print result as JSON in stdout')
    parser.add_argument('--verbose', action='store_true', help='Outputs verbose status messages')
    parser.add_argument('--limit', type=int, help='Limit news topics if this parameter provided')
    parser.add_argument('--date', type=str, help='Print cached articles by date')

    settings = parser.parse_args()

    if settings.version:
        print(f'RSS Reader {__import__(__package__).__version__}')

    if settings.verbose:
        logging.basicConfig(level=logging.INFO)
        logging.info("Logging enabled")

    RSSReader()(settings.source,
                settings.limit,
                settings.json,
                settings.date)


if __name__ == '__main__':
    main()
