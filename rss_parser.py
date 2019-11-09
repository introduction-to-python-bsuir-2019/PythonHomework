import feedparser
import json
from bs4 import BeautifulSoup
#import requests
from arg import args


def parse(args):
    return feedparser.parse(args.source)


def get_source(parsed):
    feed = parsed('item')
    return({
        'link': feed['link'],
        'title': feed['title'],
        'subtitle': feed['subtitle']
    })


def get_articles(parsed):
    articles = []
    entries = parsed['entries']
    for entry in entries:
        soup = BeautifulSoup(entry.summary, features="html.parser")
        article_img = soup.find('img')['src']
        articles.append({
            'ID': entry['id'],
            'Link': entry['link'],
            'Title': entry['title'],
            'Description': entry['summary'],
            'Published': entry['published'],
            'article IMG': article_img
        })
    return articles


def printArticles(parsed):
    if args.limit == 0:
        print('Error, argument should be more than zero')
    print('\n'+json.dumps(get_articles(parse(args))[0:args.limit], indent=3, ))


printArticles(parse(args))