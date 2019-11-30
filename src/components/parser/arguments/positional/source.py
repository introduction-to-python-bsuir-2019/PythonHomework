from src.components.parser.arguments.arguments_abstract import ArgumentsAbstract
import argparse
import urllib.request as url
import sys

class Source(ArgumentsAbstract):

    def add_argument(self):
        self._parser.add_argument(
            'source', type=self._validate_source, help='RSS URL'
        )

    def _validate_source(self, source):

        try:
            if url.urlopen(source).getcode() is not 200:
                raise argparse.ArgumentError

            return source

        except argparse.ArgumentError:
            raise argparse.ArgumentError('Server answer code is not 200')

        except (url.HTTPError, url.URLError) as e:
            raise url.URLError(f'Something wrong with your source. Please try another rss feed: {e}')
