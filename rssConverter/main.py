import argparse
from rssConverter.RssConverter import RssConverter

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
    parser.add_argument(
        '--h',
        type=bool,
        help='help printer'
    )
    args = parser.parse_args()
    if args.h:
        print()
    rss = RssConverter()
    not_parsed_news = rss.get_news('https://news.yahoo.com/rss/')
    news_list = rss.parse_news(not_parsed_news)
    rss.print_news(news_list, args.limit)
    if args.json:
        rss.in_json_format(news_list, args.limit)
