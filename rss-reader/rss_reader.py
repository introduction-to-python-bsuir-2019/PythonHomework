"""
Python RSS reader v0.8

Designed to download news from the entered url.

Opportunities:
    * Get version
    * Conversion to JSON
    * Logging
    * Limiting articles

For information enter
    "python rss_reader.py --help"
in terminal to find more information.

"""

__version__ = "v0.8"

import logging
import feedparser
import argparse

from .htmlparser import *


class RSSReader:
    def execute(self, source, verbose, limit, as_json):
        """
        Procedure executing program. Get additional setting parameters and running

        :param source: URL for downloading news articles
        :param verbose: Output the logs of program
        :param limit: Limit of output news articles
        :param as_json: Show news articles as JSON
        :type source: str
        :type verbose: bool
        :type limit: int
        :type as_json: bool
        """
        if verbose:
            logging.basicConfig(level=logging.INFO)
        logging.info("Logging enabled")
        logging.info("Getting response from %s" % source)
        response = feedparser.parse(source)

        if response.status in range(200, 300):
            logging.info("Status code %d. Getting articles from %s was successful" % (response.status, source))
        else:
            logging.info("Status code %d. Getting articles from %s was unsuccessful" % (response.status, source))

        title = self.parse_title(response)
        articles = self.parse_articles(response, limit)

        if as_json:
            self.json_print(articles, title)
        else:
            self.sample_print(articles, title)

    @staticmethod
    def json_print(articles, title):
        """
        Procedure for output articles in JSON format.

        :param articles: articles for converting to JSON
        :param title: header of RSS Source
        :type articles: dict
        :type title: dict
        """
        logging.info("Start creating JSON format of feeds")
        data = Parser.get_json(articles, title)
        logging.info("Completed. Printing..")
        print(data)

    @staticmethod
    def sample_print(articles, title):
        """
        Procedure for sample output of news articles.

        :param articles: articles for output
        :param title: header of RSS Source
        :type articles: dict
        :type title: dict
        """
        logging.info("Start creating readable format of feeds")
        if title is not None:
            print(f"Feed: {title['feed']}\n")

        for article in articles:
            logging.info("Parsing article..")
            art, links = Parser.parse_article(article)
            print(f"Title: {art['title']}\n"
                  f"Date: {art['pubDate']}\n"
                  f"Link: {art['link']}\n\n"
                  f"{art['description']}\n\n"
                  f"Links:")
            for link in links:
                print(link)
            print('################################################################################')

    @staticmethod
    def parse_title(response):
        """
        Static method for parsing header of RSS Source.

        :param response: response struct for parse
        :type response: dict
        :return: header of RSS Source if parsing was successful, else None
        :rtype: dict or None
        """
        try:
            logging.info("Successfully get Header of RSS Source: %s" % response.feed.title)
            return {'feed': response.feed.title}
        except KeyError:
            logging.info("Getting header of RSS Source was unsuccessful")
            return None

    @staticmethod
    def parse_articles(response, limit):
        """
        Parse articles from response struct.
        If limit is None return articles given length, else return all available articles.

        :param response: response struct for parse
        :param limit: limit of output news articles
        :type response: dict
        :type limit: int or None
        :return: news articles of limited length
        :rtype: dict
        """
        logging.info("Start loading articles. Limit: %d" % limit or "None")
        result = response.entries
        if limit is not None:
            logging.info("Completed. Loaded %d articles" % min(limit, len(result)))
            return result[0:min(limit, len(result))]
        else:
            logging.info("Completed. Loaded all articles")
            return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('source', action='store', type=str, help='RSS URL')
    parser.add_argument('--version', action='store_true', help='Print version info')
    parser.add_argument('--json', action='store_true', help='Print result as JSON in stdout')
    parser.add_argument('--verbose', action='store_true', help='Outputs verbose status messages')
    parser.add_argument('--limit', type=int, help='Limit news topics if this parameter provided')

    settings = parser.parse_args()

    if settings.version:
        print(f'RSS Reader {__version__}')

    RSSReader().execute(settings.source, settings.verbose, settings.limit, settings.json)


if __name__ == '__main__':
    main()
