import argparse
import feedparser
from .news import News
from .cache import Cache
import logging
import sys


version = '1.5'


def main():
    """Main function of program"""

    logger = logging.getLogger('rss_reader')
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler = logging.FileHandler('rss_reader_logs.log')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    logger.setLevel(logging.INFO)

    parser = argparse.ArgumentParser(description='Python RSS-reader')
    parser.add_argument('URL', type=str, help='RSS URL')
    parser.add_argument('--version', help='Print version info', action='version', version=version)
    parser.add_argument('--json', help='Print result as JSON in stdout', action='store_true')
    parser.add_argument('-V', '--verbose', help='Outputs verbose status messages', action='store_true')
    parser.add_argument('-L', '--limit', help='Limit news topics if this parameter is provided', type=int, default=0)
    parser.add_argument('--date', help='Find news in cache if this parameter is provided', type=int, default=0)
    parser.add_argument('--to-html', help='Create a HTML file with news', type=str, default="")
    parser.add_argument('--to-fb2', help='Create a fb2 file with news', type=str, default="")
    args = parser.parse_args()

    if args.verbose:
        stdout_handler = logging.StreamHandler(sys.stdout)
        stdout_handler.setFormatter(formatter)
        logger.addHandler(stdout_handler)

    if args.date:
        logger.info('Starting to read from cache')
        state = Cache.print_news(args.date)
        if state == 1:
            print(f'''There are not exist news with date of publication at {args.date}
            \nMake sure that your format date in %Y%m%d''', file=sys.stderr)
        else:
            logger.info('News from cache ware read')
    else:

        feeds = feedparser.parse(args.URL)

        if feeds.bozo:
            print('This is not well formed XML', file=sys.stderr)
            exit()

        else:
            logger.info('The XML file with news is received and correct')

        news = News(feeds, args.limit)
        logger.info('News is parsed')

        if args.to_html:
            news.create_html(args.to_html)

        elif args.to_fb2:
            news.create_fb2(args.to_fb2)

        elif args.json:
            print(news.to_json().decode())
            logger.info('News is displayed in stdout in a json format')
        else:
            news.print()
            logger.info('News is displayed in stdout in a readability format')

    logger.info('Program is over')


if __name__ == '__main__':
    main()
