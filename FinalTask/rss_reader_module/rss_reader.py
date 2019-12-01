#!/usr/bin/env python3

import argparse
import logging
import datetime
from dateutil.parser import parse
from rss_reader_module.module.RSSHandle import RssHandler, CacheControl
from rss_reader_module.module.convert import ConvertTo


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

    parser.add_argument('--to-html',
                        action='store',
                        type=str,
                        help='Create HTML file from RSS feed in given path')

    args = parser.parse_args()

    if args.verbose:
        logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

    if args.version:
        print('\nRSS-Reader v2.0\n')

    cache = CacheControl(args.date)

    if args.date is not None:
        if len(args.date) != 8:
            raise KeyError('Date is not valid!')
        try:
            int(args.date)
        except ValueError:
            raise KeyError('Date is not valid!')
    else:
        rss_object = RssHandler(args.source)
        for news in rss_object.feed_dict['news']:
            date_parsed = parse(news['published'])
            name = datetime.datetime.strftime(date_parsed, '%Y%m%d')
            values = news.copy()
            values['published'] = datetime.datetime.strftime(parse(news['published']), '%H%M%S')
            values['source'] = rss_object.feed_dict['Name']
            values['links'] = ' '.join(values['links'])
            values['media'] = ' '.join(values['media'])
            cache.insert_values('date'+name, tuple(values.values()))

    if args.date is not None:
        cache.cache_output(args.limit, args.json)
        convert = ConvertTo(cache.cache_dict, args.to_html)
    else:
        rss_object.output(args.json, args.limit)
        convert = ConvertTo(rss_object.feed_dict, args.to_html)

    if args.to_html is not None:
        convert.to_html()


if __name__ == '__main__':
    main()
