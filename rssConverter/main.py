from rssConverter.RssConverter import RssConverter
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Rss reader')
    parser.add_argument(
        '--limit',
        type=int,
        help='number of news you want to read'
    )
    parser.add_argument(
        '--json',
        type=bool,
        help='do you need json format'
    )
    args = parser.parse_args()
    rss = RssConverter()
    new = rss.get_news('https://news.yahoo.com/rss/', args.limit)
    rss.print_news(new)
    if args.json:
        rss.json_convert(new)
