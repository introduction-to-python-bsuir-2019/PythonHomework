#!/usr/bin/env python3
import argparse
from project.reader import RSSReader


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("--version", action='version',    help="Print version info", version="Version 0.3")
    parser.add_argument("source",    type=str,            help="RSS URL")
    parser.add_argument("--json",    action="store_true", help="Print result as JSON in stdout")
    parser.add_argument("--verbose", action="store_true", help="Outputs verbose status messages")
    parser.add_argument("--to_fb2",  action="store_true", help="Save as fb2 file")
    parser.add_argument("--to_html", action="store_true", help="Save as html file")
    parser.add_argument("--path",    type=str,            help="Save news to file at entered path.")
    parser.add_argument("--limit",   type=int,            help="Limit news topics if this parameter provided")
    parser.add_argument("--date",    type=int,            help="Start work with cached data. Format YYYYMMDD")
    return parser.parse_args()


def main():
    args = parse_arguments()
    rss = RSSReader(args.source, args.limit, args.verbose, args.date, args.path)
    used = False
    if args.json:
        rss.show_json()
        used = True
    if args.to_fb2:
        rss.save_fb2()
        used = True
    if args.to_html:
        rss.save_html()
        used = True
    if not used:
        rss.show_news()


if __name__ == "__main__":
    main()
