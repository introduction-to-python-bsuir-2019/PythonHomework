import argparse
import json
from .rss_parser import RssParser
from .rss_parser import create_logger

current_version = 0.3


def main():
    parser = argparse.ArgumentParser(description='Brand new euseand\'s RSS-parser written in Python')
    parser.version = current_version
    parser.add_argument("source", help="RSS URL")
    parser.add_argument("--version", help="Print version info", action="store_true")
    parser.add_argument("--json", help="Print result as JSON in stdout", action="store_true")
    parser.add_argument("--verbose", help="Output verbose status messages", action="store_true")
    parser.add_argument("--limit", help="Limit news topics if this parameter provided", type=int)
    parser.add_argument("--date", help="Takes date in %Y%m%d format (example: --date 20191020)"
                                       "and prints out cached news for that date", action="store_true")
    args = parser.parse_args()
    if args.verbose:
        logger = create_logger('rss-reader')
        logger.info('logging enabled.')
    verbose = args.verbose
    if args.version:
        print(f'Current version: {current_version}')
        if verbose:
            logger.info('current utility version was printed')
        exit()
    if args.limit:
        limit = args.limit
        if verbose:
            logger.info(f'news limit was set to {limit}')
    else:
        limit = 10
        if verbose:
            logger.info(f'news limit was set to {limit}')
    my_parser = RssParser(args.source, limit, verbose)
    # my_parser = RssParser("https://news.yahoo.com/rss/", 1, verbose)
    # C:\\Users\\Asus\\Documents\\GitHub\\PythonHomework\\FinalTask\\rss_reader\
    online_or_cached = ''
    if args.date:
        with open("news_cache.txt", 'r') as cache_file:
            json_to_parse = json.load(cache_file)
        my_parser.parse_json_cache(json_to_parse)
        online_or_cached += 'cached'
    else:
        my_parser.parse_rss()
        online_or_cached += 'online'
    json_feed = my_parser.feed_to_json()
    if args.json:
        print(json.dumps(json_feed, indent=1))
        if verbose:
            logger.info(f'{limit} {online_or_cached} news have been printed in JSON format')
    else:
        text_feed = ''
        text_feed += my_parser.feed_to_string()
        print(text_feed)
        if verbose:
            logger.info(f'{limit} {online_or_cached} news have been printed')
    with open("news_cache.txt", 'w') as cache_file:
        json.dump(json_feed, cache_file)
    if verbose:
        logger.info(f'{limit} news have been saved in local cache')


if __name__ == '__main__':
    main()
