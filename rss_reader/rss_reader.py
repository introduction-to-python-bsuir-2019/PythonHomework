import argparse
from Reader import Reader

VERSION_INFO = 2.0


def main():
    """
    Add args, which will be available, when you will work with console.
    """
    # http://news.yahoo.com/rss/
    # https://news.google.com/news/rss
    parser = argparse.ArgumentParser(description="Pure Python command-line RSS reader.")
    parser.add_argument("source", help="RSS URL")
    parser.add_argument("--version", help="Print version info", action="store_true")
    parser.add_argument("--json", help="Print result as JSON in stdout", action="store_true")
    parser.add_argument("--verbose", help="Output verbose status messages", action="store_true")
    parser.add_argument("--limit", help="Limit news topics if this parameter provided", type=int)
    args = parser.parse_args()
    print(args)

    if args.version:
        print("Version of the rss-reader: {0}".format(VERSION_INFO))

    reader = Reader(args.source)
    reader.is_verbose = args.verbose
    news_items = reader.get_news(args.limit)
    for news_item in news_items:
        print(news_item)

    if args.json:
        for news_item in news_items:
            print(news_item.get_json_representation())


if __name__ == '__main__':
    main()
