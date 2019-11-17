import argparse
import feedparser
from news import News
import logging
import sys

version = '1.0'


def main():
    """Main function of program"""
    logger = logging.getLogger('rss_reader')
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler = logging.FileHandler('rss_reader_logs.log')
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    parser = argparse.ArgumentParser(description='Python RSS-reader')
    parser.add_argument("URL", type=str, help='RSS URL')
    parser.add_argument("--version", help="Print version info", action="version", version=version)
    parser.add_argument("--json", help="Print result as JSON in stdout", action="store_true")
    parser.add_argument("-V", "--verbose", help="Outputs verbose status messages", action="store_true")
    parser.add_argument("-L", "--limit", help="Limit news topics if this parameter is provided", type=int, default=0)
    args = parser.parse_args()

    if args.verbose:
        stdout_handler = logging.StreamHandler(sys.stdout)
        stdout_handler.setFormatter(formatter)
        stdout_handler.setLevel(logging.INFO)
        logger.addHandler(stdout_handler)
    feeds = feedparser.parse(args.URL)

    if feeds.bozo:
        logger.error("Feed is not well-formed XML")
    else:
        logger.info("The XML file with news is received and correct")

    news = News(feeds, args.limit)
    logger.info("News is parsed")

    if args.json:
        print(news.to_json().decode())
        logger.info("News is displayed in stdout in a json format")
    else:
        news.print()
        logger.info("News is displayed in stdout in a readability format")

    logger.info("Program is over")





if __name__ == "__main__":
    main()

