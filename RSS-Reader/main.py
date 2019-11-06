import argparse
# import feedparser

from rss_parser import RssReader


VERSION = 'version 1.0'

# LINK = 'https://www.reddit.com/.rss'

LINK = 'https://news.yahoo.com/rss/'
# LINK = 'https://www.newsisfree.com/rss/'


def init_args(parser):
    parser.add_argument(
        '--version',
        help='Print version info',
        action='version',
        version=VERSION
    )

    parser.add_argument(
        '--json',
        help='Print result as JSON in stdout',
        action='store_true'
    )

    parser.add_argument(
        '--limit',
        type=int,
        help='Limit news topics if this parameter provided'
    )

    parser.add_argument(
        "link",
        type=str,
        metavar='LINK',
        help='Link on RSS resource'
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Command-line RSS reader.')
    init_args(parser)
    args = parser.parse_args()

    rss_reader = RssReader(link=LINK)

    if args.json is True:
        with open('news.json', 'w+') as file:
            file.write(rss_reader.get_news_as_json())
    elif args.link is not None:
        if args.limit is not None:
            limit = args.limit
        else:
            limit = 0

        news = rss_reader.get_news_as_string(limit=limit)    
        print(news)
