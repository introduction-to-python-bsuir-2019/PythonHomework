import argparse
import json
from datetime import datetime
from .rss_parser import RssParser

current_version = '0.420'


def main():
    """
    This function contains all utility features realisation
    :return: None
    """
    parser = argparse.ArgumentParser(description='Brand New euseand\'s RSS-parser written in Python')
    parser.version = current_version
    parser.add_argument("source", help="RSS URL to be parsed. Write empty quotes for default")
    parser.add_argument("--version", help="Print version info", action="store_true")
    parser.add_argument("--json", help="Print result as JSON in stdout", action="store_true")
    parser.add_argument("--verbose", help="Output verbose status messages", action="store_true")
    parser.add_argument("--limit", help="Limit news topics if this parameter provided", type=int)
    parser.add_argument("--date", help="Write date in %%Y%%m%%d format (example: --date 20191020)"
                                       "to print out cached news for that date", type=str)
    parser.add_argument("--to-html", help="Cache news to html file in human-readable format. "
                                          "Takes path to file including file name as argument. "
                                          "If only file name given, creates file in a current working directory. "
                                          "Write \"default\" to create a default file in package data folder", type=str)
    parser.add_argument("--to-pdf", help="Cache news to pdf file in human-readable format. "
                                         "Takes path to file including file name as argument. "
                                         "If only file name given, creates file in a current working directory. "
                                         "Write \"default\" to create a default file in package data folder", type=str)
    args = parser.parse_args()
    error_raised = False
    if args.verbose:
        logger = RssParser.create_logger('rss-reader')
        logger.info('Logging enabled.')
    if args.version:
        print(f'Current version: {current_version}')
        exit()
        if args.verbose:
            logger.info('Current utility version was printed')
    if args.limit:
        if args.limit > 0:
            limit = args.limit
            if args.verbose:
                logger.info(f'News limit was set to {limit}')
        else:
            limit = 10
            if args.verbose:
                logger.info(f'News limit was set to {limit} due to invalid limit value input')
    else:
        limit = 10
        if args.verbose:
            logger.info(f'News limit was set to {limit} as default')
    if args.source:
        source = args.source
        if args.verbose:
            logger.info(f'Utility has started with next source URL: {source}')
    else:
        source = "https://news.yahoo.com/rss/"
        if args.verbose:
            logger.info(f'Source URL was set to default: {source}')
    if args.date:
        try:
            datetime.strptime(args.date, '%Y%m%d')
        except ValueError:
            print(f'rss-reader: rss-reader.py : error: Wrong date format')
            date = datetime.strftime(datetime.now(), '%Y%m%d')
            print(f'rss-reader: rss-reader.py : info: '
                  f'Date was set to today ({date}) due to invalid date value input')
    my_parser = RssParser(source, limit, args.verbose, args.date, args.to_html, args.to_pdf)
    online_or_cached = ''
    if args.date:
        online_or_cached += 'cached'
        if args.verbose:
            logger.info(f'Cached news will be fetched')
        try:
            my_parser.parse_json_cache()
        except Exception as parse_json_exc:
            print(f'rss-reader: rss_parser.py : parse_json_cache : error : {parse_json_exc}')
            error_raised = True
    else:
        online_or_cached += 'online'
        if args.verbose:
            logger.info(f'Online news will be fetched')
        try:
            my_parser.parse_rss()
        except Exception as parse_online_feed_exc:
            print(f'rss-reader: rss_parser.py : parse_rss : error : {parse_online_feed_exc}')
            error_raised = True
        try:
            my_parser.cache_feed_to_json_file()
        except Exception as cache_to_json_exc:
            print(f'rss-reader: rss_parser.py : cache_feed_to_json_file : error : {cache_to_json_exc}')
            error_raised = True
    if not error_raised:
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
            try:
                my_parser.cache_feed_to_html_file()
            except Exception as cache_to_html_exc:
                print(f'rss-reader: rss_parser.py : cache_feed_to_html_file : error : {cache_to_html_exc}')
            if args.verbose:
                logger.info(f'{len(my_parser.news)} {online_or_cached} news have been cached in html file')
        if args.to_pdf:
            try:
                my_parser.cache_feed_to_pdf_file()
            except Exception as cache_to_pdf_exc:
                print(f'rss-reader: rss_parser.py : cache_feed_to_pdf_file : error : {cache_to_pdf_exc}')
            if args.verbose:
                logger.info(f'{len(my_parser.news)} {online_or_cached} news have been cached in pdf file')


if __name__ == '__main__':
    try:
        main()
    except Exception as main_exc:
        print(f'rss-reader: rss-reader.py : main : error: {main_exc}')
