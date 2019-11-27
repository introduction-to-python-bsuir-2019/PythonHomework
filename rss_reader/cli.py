import argparse
import logging
from datetime import datetime
from pathlib import Path
from validator_collection.checkers import is_url
from .rss_reader import RssReader


def main():
    parser = adding_arguments()
    args = parser.parse_args()
    init_logging(args.verbose)
    configuration_for_conversion = mk_config_for_conversion(args.to_pdf, args.to_html)
    rss = RssReader(args.source, args.limit, args.date, args.json, configuration_for_conversion)
    rss()


def adding_arguments():
    parser = argparse.ArgumentParser(description='Pure Python command-line RSS reader')
    parser.add_argument('source', metavar='source', type=url, help='RSS URL')
    parser.add_argument('--version', action='version', version='ver 1.2', help='Print version info')
    parser.add_argument('--limit', metavar='LIMIT', type=int)
    parser.add_argument('--verbose', action='store_true')
    parser.add_argument('--json', action='store_true')
    parser.add_argument('--date', type=date)
    parser.add_argument('--to-pdf', type=directory)
    parser.add_argument('--to-html', type=directory)
    return parser


def directory(path):
    if not Path.exists(path):
        raise ValueError('Wrong path to save file')
    return path


def url(source):
    if not is_url(source):
        raise argparse.ArgumentError('Invalid url')
    return source


def date(date):
    try:
        checked_date = datetime.strptime(date, '%Y%m%d')
        return checked_date
    except:
        raise argparse.ArgumentError('Wrong date')
    
    
def init_logging(verbose):
    if verbose:
        logging.basicConfig(format='%(module)s %(asctime)s  %(message)s',
                            datefmt='%I:%M:%S', level=logging.INFO)

def mk_config_for_conversion(pdf, html):
    from collections import defaultdict
    dict_with_directories = defaultdict(Path)
    if pdf:
        dict_with_directories['pdf'] = pdf
    if html:
        dict_with_directories['html'] = html
    return dict_with_directories


if __name__ == "__main__":
    main()
