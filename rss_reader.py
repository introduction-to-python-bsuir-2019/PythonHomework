#!/usr/bin/python3.8
import logging
from App.RSSListener import RSSListener
from App import Args_parser

if __name__ == '__main__':
    args = Args_parser.parsing_args()
    Args_parser.start_settings(args)
    logging.info("Program launch")
    rss_listener = RSSListener(args.limit, args.json)
    rss_listener.start(args.source)
