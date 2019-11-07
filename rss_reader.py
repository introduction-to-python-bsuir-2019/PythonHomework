import argparse
from Reader import Reader


def main():
    # http://news.yahoo.com/rss/
    # https://news.google.com/news/rss
    parser = argparse.ArgumentParser()
    parser.add_argument("source", help="RSS URL")
    args = parser.parse_args()
    reader = Reader(args.source)

    news_items = reader.get_news(5)
    for news_item in news_items:
        print(news_item)


if __name__ == '__main__':
    main()
