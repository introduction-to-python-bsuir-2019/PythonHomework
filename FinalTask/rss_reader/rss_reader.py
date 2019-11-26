import argparse
import json
from rss_reader import rss_parser

current_version = 0.24


def main():
    parser = argparse.ArgumentParser(description='Brand new euseand\'s RSS-parser written in Python')
    parser.version = current_version
    parser.add_argument("source", help="RSS URL")
    parser.add_argument("--version", help="Print version info", action="store_true")
    parser.add_argument("--json", help="Print result as JSON in stdout", action="store_true")
    parser.add_argument("--verbose", help="Output verbose status messages", action="store_true")
    parser.add_argument("--limit", help="Limit news topics if this parameter provided", type=int)
    args = parser.parse_args()
    if args.version:
        print(f'Current version: {current_version}')
        exit()
    if args.limit:
        limit = args.limit
    else:
        limit = 10
    verbose = args.verbose
    my_parser = rss_parser.RssParser(args.source, limit, verbose)
    if args.json:
        my_parser.parse_rss()
        print(json.dumps(my_parser.feed_to_json(), indent=1))
    else:
        print(my_parser.parse_rss())


if __name__ == '__main__':
    main()
