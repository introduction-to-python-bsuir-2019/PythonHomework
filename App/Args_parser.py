import argparse
import sys
import App
import logging


def parsing_args():
    """Парсим аргументы"""
    parser = argparse.ArgumentParser(description='Pure Python command-line RSS reader.')
    parser.add_argument('source', type=str, help='RSS URL')
    parser.add_argument('--version', action="store_true", help='Print version info')
    parser.add_argument('--json', action="store_true", help='Print result as JSON in stdout')
    parser.add_argument('--verbose', action="store_true", help='Outputs verbose status messages')
    parser.add_argument('--limit', type=int, help='Limit news topics if this parameter provided')
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
        print("Limit cannot be less than 0")
        logging.error("Limit cannot be less than 0")
        exit()
