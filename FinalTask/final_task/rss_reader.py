import argparse
from rss_parser import RssParser

current_version = 0.1

def main():
    parser = argparse.ArgumentParser(description='Brand new euseand''s RSS-parser written in Python')
    parser.version = current_version
    parser.add_argument("source", help="RSS URL")
    parser.add_argument("--version", help="Print version info", action="store_true")
    parser.add_argument("--json", help="Print result as JSON in stdout", action="store_true")
    parser.add_argument("--verbose", help="Output verbose status messages", action="store_true")
    parser.add_argument("--limit", help="Limit news topics if this parameter provided", type=int)
    args = parser.parse_args()
    print(args)

    my_parser = RssParser(args.source)
    print(my_parser.parse_rss())
