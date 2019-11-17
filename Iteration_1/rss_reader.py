import argparse
import feedparser
from bs4 import BeautifulSoup
# https://news.yahoo.com/rss/


def main():
    def rss_reader(**kwargs):
        print()
        for key, value in kwargs.items():
            if key == 'source':
                d = feedparser.parse(value)
            elif key == 'limit':
                news_limit = value

        print('Feed:', d['channel']['title'])
        print('------------------------------------------------')

        for news in d['entries'][0:news_limit]:
            title = news['title']
            print('Title:', title.replace('&#39;', "'"))
            print('Date:', news['published'])
            print('Link:', news['link'])
            print()
            soup = BeautifulSoup(news['summary'], 'html.parser')
            print('Image title:', soup.find('img')['title'])
            print('Image description:', soup.p.contents[-2])
            print('Image link:', soup.find('img')['src'])
            print('------------------------------------------------')

    parser = argparse.ArgumentParser(description='Pure Python command-line RSS reader.')
    parser.add_argument('source', type=str, help='RSS URL')
    parser.add_argument('--limit', type=int, help='Limit news topics if this parameter provided')

    args = parser.parse_args()

    rss_reader(**vars(args))


if __name__ == '__main__':
    main()
