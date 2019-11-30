import argparse
import json
from .rss_parser import RssParser
from .rss_parser import create_logger

current_version = 0.413


def main():
    parser = argparse.ArgumentParser(description='Brand New euseand\'s RSS-parser written in Python')
    parser.version = current_version
    parser.add_argument("source", help="RSS URL (leave empty quotes for default)")
    parser.add_argument("--version", help="Print version info", action="store_true")
    parser.add_argument("--json", help="Print result as JSON in stdout", action="store_true")
    parser.add_argument("--verbose", help="Output verbose status messages", action="store_true")
    parser.add_argument("--limit", help="Limit news topics if this parameter provided", type=int)
    parser.add_argument("--date", help="Write date in %Y%m%d format (example: --date 20191020)"
                                       "to print out cached news for that date", type=str)
    parser.add_argument("--to-html", help="Cache news to html file in readable format", action="store_true")
    parser.add_argument("--to-pdf", help="Cache news to pdf file in readable format", action="store_true")
    args = parser.parse_args()
    if args.verbose:
        logger = create_logger('rss-reader')
        logger.info('logging enabled.')
    if args.limit:
        limit = args.limit
        if args.verbose:
            logger.info(f'news limit was set to {limit}')
    else:
        limit = 10
        if args.verbose:
            logger.info(f'news limit was set to {limit}')
    source = args.source if args.source else "https://news.yahoo.com/rss/"
    my_parser = RssParser(source, limit, args.verbose, args.date)
    online_or_cached = ''
    if args.date:
        my_parser.parse_json_cache()
        online_or_cached += 'cached'
    else:
        my_parser.parse_rss()
        my_parser.cache_feed_to_text_file()
        online_or_cached += 'online'
    if args.json:
        print(json.dumps(my_parser.feed_to_json(), indent=1))
        if args.verbose:
            logger.info(f'{len(my_parser.news)} {online_or_cached} news have been printed in JSON format')
    else:
        text_feed = ''
        text_feed += my_parser.feed_to_string()
        print(text_feed)
        if args.verbose:
            logger.info(f'{len(my_parser.news)} {online_or_cached} news have been printed')
    if args.to_html:
        my_parser.cache_feed_to_html_file()
        if args.verbose:
            logger.info(f'{len(my_parser.news)} {online_or_cached} news have been cached in html file')
    if args.to_pdf:
        my_parser.cache_feed_to_pdf_file()
        if args.verbose:
            logger.info(f'{len(my_parser.news)} {online_or_cached} news have been cached in pdf file')
    if args.version:
        print(f'Current version: {current_version}')
        if args.verbose:
            logger.info('current utility version was printed')


if __name__ == '__main__':
    main()
