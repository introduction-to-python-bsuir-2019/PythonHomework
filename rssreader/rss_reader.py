"""
Python RSS reader

Designed to download news from the entered url.

Opportunities:
    * Get version
    * Conversion to JSON
    * Logging
    * Limiting articles
    * Caching news feeds in SQLite database
    * Converting to PDF and HTML formats
    * Print in colorize mode

For information enter
    "python3.8 rss_reader -h"
in terminal to find more information.

"""
__package__ = 'rssreader'

import argparse
import datetime
import logging

import feedparser

from rssreader.feed_parser import *
from rssreader.output_controller import *
from rssreader.storage import *


class RSSReader:
    def __call__(self, source, limit, date, **kwargs):
        """
        Procedure executing program. Get additional setting parameters and running.

        :param source: URL for downloading news articles
        :param limit: limit news topics if this parameter provided
        :param date: print cached articles by date
        :param kwargs: optional parameter for control behavior of output method.
            Use one from this parameters:
            * to_json: bool - output in JSON or not
            * to_pdf: str - string filename for output
            * to_html: str - string filename for output
            * colorize: bool - print the result in colorized mode
            Default start sample output
        :type source: str
        :type limit: int or None
        :type date: str or None
        :type kwargs: dict
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

        if len(articles['articles']) < 1:
            print(f"No news articles for output")
            exit(0)

        logging.info("All articles was successfully loaded")

        OutputController.print(articles, **kwargs)

    @staticmethod
    def _get_articles_from_url(source, limit):
        logging.info("Completed. Check the availability of URL.")

        if 'status' not in (response := feedparser.parse(source.strip())) or len(response['entries']) == 0:
            print(f"Error: Impossible parse RSS Feeds from url '{source}'")
            exit(0)

        logging.info("Completed. Check status code of response.")

        if response['status'] in range(200, 300):
            logging.info(f"Status code {response['status']}. Getting articles from '{source}' was successful")
        else:
            print(f"Error connecting with URL '{source.strip()}' with status code {response['status']}.")
            exit(0)

        return Parser.parse(response, limit)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('source', action='store', type=str, help='RSS URL')
    parser.add_argument('--version', action='store_true', help='Print version info')
    parser.add_argument('--json', action='store_true', help='Print result as JSON in stdout')
    parser.add_argument('--verbose', action='store_true', help='Outputs verbose status messages')
    parser.add_argument('--limit', type=int, help='Limit news topics if this parameter provided')
    parser.add_argument('--date', type=str, help='Print cached articles by date')
    parser.add_argument('--to-pdf', type=str, help='Print result as PDF in entered file')
    parser.add_argument('--to-html', type=str, help='Print result as HTML in entered file')
    parser.add_argument('--colorize', action='store_true', help='Print the result of the utility in colorized mode')

    settings = parser.parse_args()

    output = {
        'colorize': settings.colorize,
        'to_json': settings.json,
        'to_pdf': settings.to_pdf,
        'to_html': settings.to_html,
    }

    if settings.version:
        print(f'RSS Reader {__import__(__package__).__version__}')

    if settings.verbose:
        logging.basicConfig(level=logging.INFO)
        logging.info("Logging enabled")

    RSSReader()(settings.source,
                settings.limit,
                settings.date,
                **output)


if __name__ == '__main__':
    main()
