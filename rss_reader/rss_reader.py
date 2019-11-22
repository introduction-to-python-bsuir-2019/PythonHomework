import argparse
from functools import reduce
import os
import requests
import html
from bs4 import BeautifulSoup
import re
import feedparser
import logging
import jsonpickle
from datetime import datetime

VERSION='v1.3'

class NewsFeed:        
    def __init__(self, link):
        if link:
            logging.info('Retrieving news...')
            feed=feedparser.parse(link)
            soup=requests.get(link).text
            soup=BeautifulSoup(soup,"html5lib")
            news_separated=soup('item')
            logging.info('News retrieved, converting to readable format...')
            self.title=feed['feed']['title']
            newsdict=feed['entries']
            self.news=[]
            for index, item in enumerate(newsdict):
                self.news.append(NewsItem(item,news_separated[index]))

    def steal_title(self, subject):
        self.title=subject.title
    
    def steal_news(self, subject):
        self.news=[]
        for item in subject:
            self.news.append(NewsItem())
            self.news[-1].title=item.title
            self.news[-1].source=item.source
            self.news[-1].date=item.date
            self.news[-1].content=item.content
            self.news[-1].images=[image for image in item.images]


class NewsItem:
    def __init__(self,*args):
        if args:
            self.title=ultimately_unescape(args[0]['title'])
            self.source=ultimately_unescape(args[0]['link'])
            self.date=ultimately_unescape(args[0]['published'])
            self.content=ultimately_unescape(clear_tags(args[0]['summary']))
            self.images=[ultimately_unescape(link['href']) for link in args[0]['links'] if 'image' in link['type']]
            self.images+=find_images(ultimately_unescape(str(args[1])))
            try:
                self.images+=[media['url'] for media in args[0]['media_content'] if 'image' in media['type']]
            except KeyError:
                pass
            self.images=[image for index, image in enumerate(self.images) if self.images.index(image)==index and image]

    def show_fields(self):
        print('\n\n'+'Title: '+self.title)
        print('Link: '+self.source)
        print('Date: '+self.date)
        print('\n'+self.content)
        print('\nImages: ')
        for number, image in enumerate(self.images):
            print('['+str(number+1)+'] '+image)


def append_existing(appendee, frame, content):
    appendee.append(NewsFeed(None))
    appendee[-1].steal_title(frame)
    appendee[-1].steal_news(content)
    return appendee

def clear_tags(text):
    logging.info('Sweeping the main content...')
    while text.find('<')>-1 and text.find('>')>-1:
        text=text.replace(text[text.find('<'):text.find('>')+1],'')
    return text

def cut_news_off(limit, feed):
    total_news=reduce(lambda x,y: x+y, [len(item.news) for item in feed])
    if not limit or total_news<limit:
        return feed
    left_out=0
    while total_news>=limit:
        left_out-=1
        total_news=reduce(lambda x,y: x+y, [len(item.news) for item in feed[:left_out]]) if feed[:left_out] else 0
    news_to_add=feed[left_out].news[:limit-total_news]
    new_feed=feed[:left_out]
    return append_existing(new_feed,feed[left_out], news_to_add)

def date_to_filename(news):
    try:
        return datetime.strptime(news.date, '%a, %d %b %Y %H:%M:%S %z').strftime('%Y%m%d')
    except ValueError:
        return datetime.strptime(news.date, '%d %b %Y %H:%M:%S %z').strftime('%Y%m%d')


def find_images(text):
    logging.info('Searching for additional images...')
    res=[]
    occurences=re.finditer('<img',text)
    tags=[(text.rfind('<',0,item.start()+2),text.find('>',item.start()+2)) for item in occurences]
    where_links_start=[text.find('src',start,end)+5 for start, end in tags]
    borders=[(start,text.find('"',start)) for start in where_links_start]
    res+=[text[opener:closer] for opener, closer in borders]
    return res

def get_all_filenames(news):
    return list(set(date_to_filename(item) for item in news))

def hide_object_info(news):
    return list(map(hide_object_info_util,news))

def hide_object_info_util(item):
    while item.find('"py/object": ')>-1:
        cutfrom=item.find('"py/object": ')
        item=item.replace(item[cutfrom:item.find(',',cutfrom)+2],'',1)
    return item

def insert_cache(cache_files, cache):
    jsonpickle.set_encoder_options('json', ensure_ascii=False)
    for date, cached_content in zip(cache_files, cache):
        with open('cache/'+date+'.json','w') as cache:
            cache.write(jsonpickle.encode(cached_content))

def make_json(news):
    logging.info('Converting to JSON...')
    jsonpickle.set_encoder_options('json', ensure_ascii=False)
    return [jsonpickle.encode(item) for item in news]

def parse_arguments():
    parser=argparse.ArgumentParser(description='Pure Python command-line RSS reader.')
    exclusive=parser.add_mutually_exclusive_group()
    parser.add_argument('--json',action='store_true', help='Print result as JSON in stdout')
    parser.add_argument('--verbose',action='store_true',help='Outputs verbose status messages')
    parser.add_argument('--limit', type=int,action='store',help='Limit news topics if this parameter provided')
    exclusive.add_argument('--version',action='store_true',help='Print version info')
    exclusive.add_argument('source',nargs='?',help='RSS URL',default=None)
    exclusive.add_argument('--date',nargs='?', type=str, action='store', help='Print news posted at a certain date', default=None)
    return parser.parse_args()

def print_news(news):
    try:
        for source in news:
            print('\nSource: '+source.title)
            for item in source.news:
                item.show_fields()
    except (AttributeError, TypeError):
        print(hide_object_info(news))

def retrieve_cached_news(filenames):
    logging.info('Retrieving cached news...')
    cached=[]
    for filename in filenames:
        try:
            with open('cache/'+filename+'.json','r') as cache:
                cached.append(jsonpickle.decode(cache.read()))
        except FileNotFoundError:
            with open('cache/'+filename+'.json','w') as cache:
                cache.write(jsonpickle.encode([]))
            cached.append([])
    return cached

def ultimately_unescape(text):
    logging.info('Unescaping HTML characters...')
    while html.unescape(text)!=text:
        text=html.unescape(text)
    return text

def update_cache(fresh_news, dates, cached):
    logging.info('Caching retrieved news...')
    for date, cached_content in zip(dates, cached):
        news_to_append=[item for item in fresh_news[0].news if date_to_filename(item)==date]
        cached_source=None
        for source in cached_content:
            if source.title==fresh_news[0].title:
                cached_source=source
        if cached_source:
            cached_links=[item.source for item in cached_source.news]
            cached_source.news+=[news for news in news_to_append if news.source not in cached_links]
        else:
            cached_content=append_existing(fresh_news[0], news_to_append)
    return cached
               
def main():
    args=parse_arguments()
    if args.version and (args.json or args.limit):
        raise ValueError('You don\'t use --version together with other arguments')
    if not (args.version or args.source or args.date):
        raise ValueError('Source, --date or --version expected')
    if args.limit and args.limit<1:
        raise ValueError('Incorrect limit input (likely to be non-positive)')
    if args.version:
        print('RSS-reader '+VERSION)
    else:
        if args.verbose:
            logging.basicConfig(level=logging.INFO, 
                                format='%(asctime)s - %(message)s',
                                datefmt='%H:%M:%S')
        try:
            os.mkdir('cache')
            logging.info('Cache folder successfully created')
        except FileExistsError:
            pass
        feed=[]
        if args.date:
            try:
                datetime.strptime(args.date, '%Y%m%d')
                with open('cache/'+args.date+'.json','r') as cache:
                    feed=retrieve_cached_news([args.date])[0]
            except ValueError:
                raise ValueError('Incorrect date input')
            except FileNotFoundError:
                raise FileNotFoundError('There is no cached news for this date')
        else:
            feed=[NewsFeed(args.source)]
            cache_files=get_all_filenames(feed[0].news)
            cached=retrieve_cached_news(cache_files)
            cached=update_cache(feed, cache_files, cached)
            insert_cache(cache_files, cached)
            #feed[0].news=cut_news_off(args.limit, feed)
        feed=cut_news_off(args.limit, feed)
        if args.json:
            feed=make_json(feed)
        print_news(feed)

if __name__=='__main__':
    main()
