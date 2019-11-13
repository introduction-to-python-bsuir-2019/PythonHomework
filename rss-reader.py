from argparser import ArgParser
from RSSreader import RSSreader


def main():
    args = ArgParser()
    rss_reader = RSSreader()

    rss_reader.print_feed(rss_reader.get_feed(args.get_args()))


if __name__ == '__main__':
    main()