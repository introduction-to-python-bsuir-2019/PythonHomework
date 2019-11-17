#!/usr/bin/env python3.8
import logging
from App.RSSListener import RSSListener
from App import Args_parser


def main():
    args = Args_parser.parsing_args()
    Args_parser.start_settings(args)
    logging.info("Program launch")
    rss_listener = RSSListener(args.limit, args.json)
    rss_listener.start(args.source)


if __name__ == '__main__':
    main()
