import argparse
import requests
import html
from bs4 import BeautifulSoup
import re
import json
import feedparser
import logging
import jsonpickle

def parse_arguments():
    parser=argparse.ArgumentParser(description='Pure Python command-line RSS reader.')
    exclusive=parser.add_mutually_exclusive_group()
    parser.add_argument('--json',action='store_true', help='Print result as JSON in stdout')
    parser.add_argument('--verbose',action='store_true',help='Outputs verbose status messages')
    parser.add_argument('--limit', type=int,action='store',help='Limit news topics if this parameter provided')
    exclusive.add_argument('--version',action='store_true',help='Print version info')
    exclusive.add_argument('source',nargs='?',help='RSS URL',default=None)
    return parser.parse_args()

VERSION='v1.2'

class NewsFeed:        
    def __init__(self, link, limit):
        logging.info('Retrieving news...')
        feed=feedparser.parse(link)
        soup=requests.get(link).text
        soup=BeautifulSoup(soup,"html5lib")
        news_separated=soup('item')
        logging.info('News retrieved, converting to readable format...')
        self.title=feed['feed']['title']
        newsdict=feed['entries']
        self.news=[]
        for index, item in (enumerate(newsdict[:min(limit,len(newsdict))]) if limit else enumerate(newsdict)):
            self.news.append(NewsItem(item,news_separated[index]))

    def __add__(self, feed):
        if self.title==feed.title:
            self.news=allow_unique(self.news+feed.news)
        return self


class NewsItem:
    def __init__(self,content,soup):
        self.title=ultimately_unescape(content['title'])
        self.source=ultimately_unescape(content['link'])
        self.date=ultimately_unescape(content['published'])
        self.content=ultimately_unescape(clear_tags(content['summary']))
        self.images=[ultimately_unescape(link['href']) for link in content['links'] if 'image' in link['type']]
        self.images+=find_images(ultimately_unescape(str(soup)))
        try:
            self.images+=[media['url'] for media in content['media_content'] if 'image' in media['type']]
        except KeyError:
            pass
        self.images=[image for index, image in enumerate(self.images) if self.images.index(image)==index]

    def show_fields(self):
        print('\n\n'+'Title: '+self.title)
        print('Link: '+self.source)
        print('Date: '+self.date)
        print('\n'+self.content)
        print('\nImages: ')
        for number, image in enumerate(self.images):
            print('['+str(number+1)+'] '+image)


def allow_unique(list_of_objects):
    new_list=[]
    sources=set()
    for item in list_of_objects:
        if item.source not in sources:
            new_list.append(item)
            sources.add(item.source)
    return new_list

def ultimately_unescape(text):
    while html.unescape(text)!=text:
        text=html.unescape(text)
    return text

def find_images(text):
    logging.info('Searching for additional images...')
    res=[]
    occurences=re.finditer('<img',text)
    tags=[(text.rfind('<',0,item.start()+2),text.find('>',item.start()+2)) for item in occurences]
    where_links_start=[text.find('src',start,end)+5 for start, end in tags]
    borders=[(start,text.find('"',start)) for start in where_links_start]
    res+=[text[opener:closer] for opener, closer in borders]
    return res

def clear_tags(text):
    logging.info('Sweeping the main content...')
    while text.find('<')>-1 and text.find('>')>-1:
        text=text.replace(text[text.find('<'):text.find('>')+1],'')
    return text

def retrieve_news(link, limit):
    logging.info('Retrieving news...')
    feed=feedparser.parse(link)
    soup=requests.get(link).text
    soup=BeautifulSoup(soup,html.parser)
    news_separated=soup('item')
    logging.info('News retrieved, converting to readable format...')
    print('\nSource: '+feed['feed']['title'])
    newsdict=feed['entries']
    news=[]
    for index, item in (enumerate(newsdict[:min(limit,len(newsdict))]) if limit else enumerate(newsdict)):
        news.append(NewsItem(item,news_separated[index]))
    return news

def make_json(news):
    logging.info('Converting to JSON...')
    jsonpickle.set_encoder_options('json', ensure_ascii=False)
    return jsonpickle.encode(news)
            
def print_news(news):
    try:
        for source in news:
            print('\nSource: '+source.title)
        for item in source.news:
            item.show_fields()
    except (AttributeError, TypeError):
        print(hide_object_info(news))

def hide_object_info(news):
    while '"py/object": ' in news:
        cutfrom=news.find('"py/object": ')
        news=news.replace(news[cutfrom:news.find(',',cutfrom)+2],'',1)
    return news

def main():
    args=parse_arguments()
    if args.version and (args.json or args.limit):
        raise ValueError('You don\'t use --version together with other arguments')
    if not (args.version or args.source):
        raise ValueError('Source or --version expected')
    if args.limit and args.limit<1:
        raise ValueError('Incorrect limit input (likely to be non-positive)')
    if args.version:
        print('RSS-reader '+VERSION)
    else:
        if args.verbose:
            logging.basicConfig(level=logging.INFO, 
                                format='%(asctime)s - %(message)s',
                                datefmt='%H:%M:%S')
        feed=[NewsFeed(args.source, args.limit)]
        if args.json:
            feed=make_json(feed)
        print_news(feed)

if __name__=='__main__':
    main()
