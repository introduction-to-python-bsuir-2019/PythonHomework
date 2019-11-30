import argparse
import sys
import App
import logging
from App.Errors import FatalError


def parsing_args():
    """Парсим аргументы"""
    parser = argparse.ArgumentParser(description='Pure Python command-line RSS reader.')
    parser.add_argument('source', type=str, help='RSS URL')
    parser.add_argument('--version', action="store_true", help='Print version info')
    parser.add_argument('--json', action="store_true", help='Print result as JSON in stdout')
    parser.add_argument('--verbose', action="store_true", help='Outputs verbose status messages')
    parser.add_argument('--limit', type=int, help='Limit news topics if this parameter provided')
    parser.add_argument('--date', type=str, help='Date for which you want to display news (format %y%m%d)')
    parser.add_argument('--to_html', type=str, help='Convert data to html to your path')
    parser.add_argument('--to_pdf', type=str, help='Convert data to pdf to your path')
    return parser.parse_args()


def start_settings(args):
    """Проверяем аргументы и действуем согласно их сценарию"""
    if args.version:
        print("*" * 50 + "\n" + "Version: " + App.__version__ + "\n" + "*" * 50 + "\n" * 2)
    if args.verbose:
        logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.CRITICAL)
    if args.limit is not None and args.limit < 0:
        raise FatalError("Limit cannot be less than 0")
    if args.date is not None and (len(args.date) != 8 or args.date.isdigit() is False):
        raise FatalError("Invalid date format")
