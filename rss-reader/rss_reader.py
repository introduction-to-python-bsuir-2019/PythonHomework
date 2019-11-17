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

from htmlparser import *


class RSSReader:
    def execute(self, source, verbose, limit, as_json):
        """
        Procedure executing program. Get additional setting parameters and running.

        :param source: URL for downloading news articles
        :param verbose: output the logs of program
        :param limit: limit of output news articles
        :param as_json: show news articles as JSON
        :type source: str
        :type verbose: bool
        :type limit: int
        :type as_json: bool
        """
        if verbose:
            logging.basicConfig(level=logging.INFO)
        logging.info("Logging enabled")
        logging.info(f"Getting response from {source}")
        if 'status' not in (response := feedparser.parse(source.strip())) or len(response.entries) == 0:
            print(f"Error: Impossible parse RSS Feeds from url '{source}'")
            exit(0)

        if response.status in range(200, 300):
            logging.info(f"Status code {response.status}. Getting articles from {source} was successful")
        else:
            logging.info(f"Status code {response.status}. Getting articles from {source} was unsuccessful")

        if as_json:
            self.json_print(response, limit)
        else:
            self.sample_print(response, limit)

    @staticmethod
    def json_print(response, limit):
        """
        Procedure for output articles in JSON format.

        :param response: response struct for parse
        :param limit: required number of articles to show
        :type response: dict
        :type limit: int
        """
        logging.info("Start creating JSON format of feeds")
        data = Parser.get_json(response, limit)
        logging.info("Completed. Printing..")
        print(data)

    @staticmethod
    def sample_print(response, limit):
        """
        Procedure for sample output of news articles.

        :param response: response struct for parse
        :param limit: required number of articles to show
        :type response: dict
        :type limit: int
        """
        title, articles = Parser.parse_all(response, limit)
        logging.info("Start creating readable format of feeds")
        if title is not None:
            print(f"Feed: {title['feed']}\n")

        for article in articles:
            logging.info("Parsing article..")

            print(f"Title: {article.title}\n"
                  f"Date: {article.pubDate}\n"
                  f"Link: {article.link}\n\n"
                  f"{article.description}\n\n"
                  f"Links:")
            for link in article.links:
                print(link)
            print('################################################################################')


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

    if settings.limit < 1:
        print(f"Error: Impossible parse 0 and less RSS Feeds")
        exit(0)

    RSSReader().execute(settings.source, settings.verbose, settings.limit, settings.json)


if __name__ == '__main__':
    main()
