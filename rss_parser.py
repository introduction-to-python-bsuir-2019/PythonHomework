import feedparser
import json
from bs4 import BeautifulSoup
from arg import args
from loggerfile import logger
from cache import csv_writer, test

def parse(args):
    '''Returns URL ADDRESS'''
    return feedparser.parse(args.source)


def get_source(parsed):
    '''Gets link, title and subtitle from the executing URL'''
    feed = parsed['feed']
    return ({
        'link': feed['link'],
        'title': feed['title'],
        'subtitle': feed['subtitle']
    })


def get_articles(parsed):
    '''Gets information from the article and returns this'''
    articles = []
    entries = parsed['entries']
    try:
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
                'article IMG': article_img,
            })
    finally:
        for entry in entries:
            text = BeautifulSoup(entry.summary, features='html.parser').text
            articles.append({
                'ID': entry['id'],
                'Link': entry['link'],
                'Title': entry['title'].replace('&#39;', "'"),
                'Description': text,
                'Published': entry['published'],
            })
        return articles


def printArticles(parsed):
    '''Function to output information'''
    articles = get_articles(parsed)
    feed = get_source(parsed)
    if args.limit == 0:
        print('Error, argument should be more than zero')
    else:
        print('----------' + feed['title'] + '----------\n')
        print('URL ADDRESS: ' + feed['link'] + '\n')
        print(feed['subtitle'])
        for article in articles[0:args.limit]:
            print("\nTitle: ", article['Title'])
            print("Date: ", article['Published'])
            print("Link: ", article['Link'])
            print("\nDescription: ", article['Description'])
            try:
                print("\nImage: ", article['article IMG'])
            except:
                print('\nNo images given')
            print('\n')


def printArticlesDueToJson(parsed):
    '''Function to output information in JSON format'''
    feed = get_source(parsed)
    if args.limit == 0:
        print('Error, argument should be more than zero')
    else:
        print('----------' + feed['title'] + '----------')
        print('URL ADDRESS: ' + feed['link'] + '')
        print(feed['subtitle'])
        print(json.dumps(get_articles(parse(args))[0:args.limit], indent=3, ensure_ascii=False, ))


def logs(parsed):
    '''Logs output'''
    logger.info('Program started with source: ' + parsed['link'])
    logger.info('Limit is {}'.format(args.limit))


def versionInfo(args):
    print("Second version")


def news_caching(parsed):
    with open('data.json', 'a', encoding='utf-8') as f:
        json.dump(parsed, f, indent=3, ensure_ascii=False, )


def main():
    if args.verbose:
        print(logs(get_source(parse(args))))
    if args.version:
        versionInfo(parse(args))
    if args.json:
        printArticlesDueToJson(parse(args))
    else:
        printArticles(parse(args))
        news_caching(get_articles(parse(args)))


if __name__ == "__main__":
    main()
