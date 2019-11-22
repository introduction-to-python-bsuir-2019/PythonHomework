import argparse
import logging
import datetime
from validator_collection.checkers import is_url
from .rss_reader import RssReader


def main():
    parser = adding_arguments()
    args = parser.parse_args()
    init_logging(args.verbose)
    validation(args.source)
    rss = RssReader(args.source, args.limit, args.date, args.json)
    rss.get_news()
    #rss.print_news()


def adding_arguments():
    parser = argparse.ArgumentParser(description='Pure Python command-line RSS reader')
    parser.add_argument('source', metavar='source', type=str, help='RSS URL')
    parser.add_argument('--version', action='version', version='ver 1.2', help='Print version info')
    parser.add_argument('--limit', metavar='LIMIT', nargs=1, type=int)
    parser.add_argument('--verbose', action='store_true')
    parser.add_argument('--json', action='store_true')
    parser.add_argument('--date', nargs=1, type=str)
    return parser


def init_logging(verbose):
    if verbose:
        logging.basicConfig(format='%(module)s %(asctime)s  %(message)s',
                            datefmt='%I:%M:%S', level=logging.INFO)


def validation(url, date=None):
    logging.info('Validate input parameters')
    try:
        if date:
            date_structure = datetime.strptime(date, '%Y%m%d')
        if is_url(url):
            return url, date
        else:
            raise Exception('Invalid url')
    except Exception as e:
        logging.error(e)


if __name__ == "__main__":
    main()
