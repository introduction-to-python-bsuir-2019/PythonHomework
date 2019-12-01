#!/usr/bin/env python3.8
import logging
from App.RSSListener import RSSListener
from App import Args_parser
from termcolor import colored
from App.Colors import Colors


def main():
    try:
        args = Args_parser.parsing_args()
        Args_parser.start_settings(args)
        logging.info("Program launch")
        rss_listener = RSSListener(args.limit, args.json, args.date, args.to_html, args.to_pdf)
        rss_listener.start(args.source)
    except Exception as e:
        print(colored(str(e), Colors["error"]))
        close_program()


def close_program():
    print(colored("The program suddenly completed its work", Colors["error"]))
    exit()


if __name__ == '__main__':
    main()
