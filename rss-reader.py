from argparser import ArgParser
from RSSreader import RSSreader


def main():
    args = ArgParser()
    rss_reader = RSSreader(args)
    feed = rss_reader.get_feed()
    if args.get_args().json:
        rss_reader.print_feed_json(feed)
    else:
        rss_reader.print_feed(feed)


if __name__ == '__main__':
    main()
