'''Module implements a CLI of the application'''
import logging
from argparse import ArgumentParser
from datetime import datetime
from os import path, makedirs
from validator_collection.checkers import is_url
from .rssreader import RSSReader
from collections import defaultdict


def main():
    '''Entry point of the app'''
    parser = adding_arguments()
    args = parser.parse_args()
    init_logging(args.verbose)
    source, date = validate_arguments(args)
    configuration_for_conversion = mk_config_for_conversion(args.to_pdf, args.to_html)
    rss = RSSReader(source, args.limit, date, args.json, configuration_for_conversion, args.all)
    rss.exec()


def adding_arguments():
    '''Function initializes arguments of the RSS Reader'''
    parser = ArgumentParser(description='Pure Python command-line RSS reader')
    parser.add_argument('source', metavar='source', type=str, help='RSS URL')
    parser.add_argument('--version', action='version', version='ver 1.4', help='Print version info')
    parser.add_argument('--limit', metavar='LIMIT', type=int, help='Amount of news output')
    parser.add_argument('--verbose', action='store_true', help='Print all logs in stdout')
    parser.add_argument('--json', action='store_true', help='Print news in json format')
    parser.add_argument('--date', type=str, help='Print news published on a given day')
    parser.add_argument('--to-pdf', type=str, help='Conversion news to the PDF format')
    parser.add_argument('--to-html', type=str, help='Conversion news to the HTML format')
    parser.add_argument('--all', action='store_true', help='Getting all cached news.\
                    Compatible with the following arguments: --verbose, --json, --to-pdf, --to-html')
    return parser


def init_logging(verbose):
    '''Logging initialization'''
    if verbose:
        logging.basicConfig(format='%(module)s %(asctime)s  %(message)s',
                            datefmt='%I:%M:%S', level=logging.INFO)
        

def validate_arguments(args):
    '''Function validates of all received arguments'''
    source = validate_url(args.source)
    date = None
    if args.date:
        date = validate_date(args.date)
    if args.to_html:
        validate_path(args.to_html)
    if args.to_pdf:
        validate_path(args.to_pdf)
    return source, date


def validate_url(source):
    '''Function validates the URL that is the source of the news'''
    logging.info('URL validation')
    if not is_url(source):
        raise ValueError('Invalid url')
    return source


def validate_date(date):
    '''Function validates date'''
    logging.info('Date validation')
    try:
        checked_date = datetime.strptime(date, '%Y%m%d').date()
        return checked_date
    except ValueError as e:
        print('Wrong date')
        

def validate_path(dir_for_save):
    '''Function validates the path where the exported file will be saved'''
    if path.exists(dir_for_save):
        logging.info(f'Directory {dir_for_save} already exists')
    else:
        makedirs(dir_for_save)
        logging.info(f'Create directory {dir_for_save} for saving file')
    return dir_for_save


def mk_config_for_conversion(pdf, html):
    '''Function creates a dictionary which contain which type of files and where news will be saved'''
    logging.info('Making dict with configuration of conversion')
    dict_with_directories = defaultdict(str)
    if pdf:
        dict_with_directories['pdf'] = pdf
    if html:
        dict_with_directories['html'] = html
    return dict_with_directories


if __name__ == "__main__":
    main()
