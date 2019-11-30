import argparse
import logging

from .rss_reader import Reader


def main():
    args = parse_args()

    if args.verbose:
        logging.basicConfig(format="%(levelname)s: %(message)s", level=logging.INFO)
    else:
        logging.basicConfig(format="%(levelname)s: %(message)s")

    reader = Reader(args.source, args.limit, args.json, args.date)
    reader.parse_url()

    reader.print_news()


def parse_args():
    parser = argparse.ArgumentParser(description='Pure Python command-line RSS reader.')

    parser.add_argument('source', help='RSS URL')
    parser.add_argument('--version', help='Print version info', action='version', version='%(prog)s 0.2')
    parser.add_argument('--json', help='Print result as JSON in stdout', action='store_true')
    parser.add_argument('--verbose', help='Outputs verbose status messages', action='store_true')
    parser.add_argument('--limit', help='Limit news topics if this parameter provided', type=int)
    parser.add_argument('--date', help='Show cached news by input date', type=str)

    return parser.parse_args()


if __name__ == '__main__':
    main()
