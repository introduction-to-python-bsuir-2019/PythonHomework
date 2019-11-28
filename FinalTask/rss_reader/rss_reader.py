#!/usr/bin/env python3

import argparse
import logging
import datetime
from dateutil.parser import parse
from rss_reader.RSSHandle import RssHandler, CacheControl


def main():
    parser = argparse.ArgumentParser(description="Pure Python command-line RSS reader.")

    group = parser.add_mutually_exclusive_group(required=True)

    group.add_argument('--source',
                       action='store',
                       type=str,
                       help='RSS URL')

    parser.add_argument('--version',
                        action='store_true',
                        help='Print version info')

    parser.add_argument('--json',
                        action='store_true',
                        help='Print result as JSON in stdout')

    parser.add_argument('--verbose',
                        action='store_true',
                        help='Outputs verbose status messages')

    parser.add_argument('--limit',
                        action='store',
                        type=int,
                        help='Limit news topics if this parameter provided')

    group.add_argument('--date',
                       action='store',
                       type=str,
                       help='Print cached news that was published on given date')

    args = parser.parse_args()

    if args.verbose:
        logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

    if args.version:
        print('\nRSS-Reader v2.0\n')

    rss_object = RssHandler(args.source)
    cache_out = CacheControl(args.date)
    cache_in = CacheControl()

    for news in rss_object.feed_dict['news']:
        date_parsed = parse(news['pubDate'])
        name = datetime.datetime.strftime(date_parsed, '%Y%m%d')
        values = news.copy()
        values['pubDate'] = datetime.datetime.strftime(parse(news['pubDate']), '%H%M%S')
        values['source'] = rss_object.feed_dict['source']
        values['links'] = ' '.join(values['links'])
        values['media'] = ' '.join(values['media'])
        cache_in.insert_values('date'+name, tuple(values.values()))

    if args.date is not None:
        cache_out.cache_output(args.limit)
    else:
        rss_object.output(args.json, args.limit)


if __name__ == '__main__':
    main()
