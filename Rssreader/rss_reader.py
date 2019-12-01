import logging
import argparse
from Rssreader.SourseReader import NewsReader
from Rssreader.cash import StoreCashSql
from Converters.parserXML import FB2
PROJECT_VERSION = 'Version 1.5 : '
PROJECT_STATUS = 'Completed'


def Main():
    parser = argparse.ArgumentParser(prog='RSS-READER', description=' Provide simple "one shot" RSS Reader')
    parser.add_argument('url', help='Provide url please', type=str)
    parser.add_argument('--version', help='Show initial version', action='store_true')
    parser.add_argument('--json', help='Convert output to json', action='store_true')
    parser.add_argument('--verbose', help='Outputs verbose status messages', action='store_true')
    parser.add_argument('--date', help='Outputs news that was previously added to cashe by date in Ymd format',
                        type=int)
    parser.add_argument('--limit', default=6,
                        help='Limit news topics if this parameter provided.Default value is 3', type=int)
    parser.add_argument('--fb2', help='Create fb2 file.File path and name need to be provided ', type=str)
    parser.add_argument('--html', help='Create html file.Please provide file path and name ', type=str)
    args = parser.parse_args()

    news = NewsReader(args.url, args.limit)
    cash = StoreCashSql(args.url)
    if args.verbose:
        logging.basicConfig(level=logging.INFO, format='%(relativeCreated)6d %(threadName)s %(message)s')

    if args.version:
        print(PROJECT_VERSION + PROJECT_STATUS, end='\n')
        return

    elif args.json:
        for item in news.make_json():
            print(item)

    elif args.date:
        cash.show_logs(args.url, args.date, args.limit)

    elif args.fb2:
        try:
            FB2().get_news_as_fb2(news.parse_rss(), args.fb2, news.desc_of_resourse())
        except NameError:
            logging.info('FB2 converting failed in case of unavailable data')

    elif args.html:
        news.json_html(args.html)

    else:
        news.print_rss()
        try:
            cash.SqlCashing(news.parse_rss())
        except NameError:
            logging.info('SqlCashing failed in case of no data were given')


if __name__ == '__main__':
    Main()
