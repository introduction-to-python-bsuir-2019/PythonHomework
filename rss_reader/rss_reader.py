import argparse
import feedparser
import html
import re


version = '1.0'


def clean_from_tags(text_with_tags):
    return re.sub('<.*?>', '', text_with_tags)


def show_news(entries, limit):
    real_limit = len(entries)
    if limit > 0:
        if limit < len(entries):
            real_limit = limit
    for i in range(real_limit):
        print("Title:", html.unescape(entries[i].title))
        print("Data:", html.unescape(entries[i].published))
        print("Link:", entries[i].link, "\n")
        print("Description:", clean_from_tags(html.unescape(entries[i].description)), "\n")


def main():
    parser = argparse.ArgumentParser(description='Python RSS-reader')
    parser.add_argument("URL", type=str, help='RSS URL')
    parser.add_argument("--version", help="Print version info", action="version", version=version)
    parser.add_argument("--json", help="Print result as JSON in stdout", action="store_true")
    parser.add_argument("-V", "--verbose", help="Outputs verbose status messages", action="store_true")
    parser.add_argument("-L", "--limit", help="Limit news topics if this parameter is provided", type=int, default=0)
    args = parser.parse_args()
    feeds = feedparser.parse(args.URL)
    print("\n", "Feed: ", feeds.feed.title, "\n")
    show_news(feeds.entries, args.limit)


if __name__ == "__main__":
    main()

