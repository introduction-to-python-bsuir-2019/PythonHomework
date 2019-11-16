import feedparser
import json
from bs4 import BeautifulSoup
from arg import args
import loggerfile

def parse(args):
    return feedparser.parse(args.source)


def get_source(parsed):
    feed = parsed['feed']
    return({
        'link': feed['link'],
        'title': feed['title'],
        'subtitle': feed['subtitle']
    })

def get_articles(parsed):
    articles = []
    entries = parsed['entries']
    for entry in entries:
      img = BeautifulSoup(entry.summary, features="html.parser")
      article_img = img.find('img')['src']
      text = BeautifulSoup(entry.summary, features='html.parser').text
      articles.append({
            'ID': entry['id'],
            'Link': entry['link'],
            'Title': entry['title'].replace('&#39;', "'"),
            'Description': text,
            'Published': entry['published'],
            'article IMG': article_img
        })
    return articles


def printArticles(parsed):
    articles = get_articles(parsed)
    feed = get_source(parsed)
    if args.limit == 0:
        print('Error, argument should be more than zero')
    else:
        print('----------' + feed['title'] + '----------\n')
        print('URL ADRESS: ' + feed['link'] + '\n')
        print(feed['subtitle'])
        for article in articles[0:args.limit]:
            print("\nTitle: ", article['Title'])
            print("Date: ", article['Published'])
            print("Link: ", article['Link'])
            print("\nDesciption: ", article['Description'])
            #print("\nImage: ", article['article IMG'])
            print('\n')


def printArticlesDueToJson(parsed):
    feed = get_source(parsed)
    if args.limit == 0:
        print('Error, argument should be more than zero')
    else:
        print('----------'+feed['title']+'----------')
        print('URL ADDRESS: '+feed['link']+'')
        print(feed['subtitle'])
        print(json.dumps(get_articles(parse(args))[0:args.limit], indent=3, ))


def main():
    if args.json:
        printArticlesDueToJson(parse(args))
    else:
        printArticles(parse(args))


if __name__ == "__main__":
    main()