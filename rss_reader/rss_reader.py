import argparse
from bs4 import BeautifulSoup
from datetime import datetime
import feedparser
from fpdf import FPDF
from functools import reduce
import html
import jsonpickle
import logging
import os
import re
import requests

VERSION='v1.3'

class NewsFeed:        
    '''A class that represents news from a specific source. Includes source name and list of retrieved news.'''
    def __init__(self, link):
        '''If link is provided, this method tries to retrieve news and source name from it, does nothing if None'''
        if link:
            logging.info('Retrieving news...')
            feed=feedparser.parse(link)
            soup=requests.get(link).text
            soup=BeautifulSoup(soup,"html5lib")
            news_separated=soup('item')
            logging.info('News retrieved, converting to readable format...')
            self.title=feed['feed']['title']
            newsdict=feed['entries']
            self.news=[NewsItem(item, news_separated[index]) for index, item in enumerate(newsdict)]

    def steal_title(self, subject):
        '''Copies source name from an existing object.'''
        self.title=subject.title
    
    def steal_news(self, subject):
        '''Inserts a given list of news into object's news list'''
        self.news=[]
        for item in subject:
            self.news.append(NewsItem())
            self.news[-1].title=item.title
            self.news[-1].source=item.source
            self.news[-1].date=item.date
            self.news[-1].content=item.content
            self.news[-1].images=[image for image in item.images]


class NewsItem:
    '''Represents a certain news article'''
    def __init__(self,*args):
        """Either takes none (creates an "empty" object) or 2 arguments (using more won't change anything)

        In case of 2 arguments takes feedparser and BeautifulSoup items.
        feedparser item is used to fill in content while BeautifulSoup is used to search for additional images
        """
        if args:
            self.title=ultimately_unescape(args[0]['title'])
            self.source=ultimately_unescape(args[0]['link'])
            self.date=ultimately_unescape(args[0]['published'])
            self.content=ultimately_unescape(hide(args[0]['summary'],'<','>'))
            self.images=[ultimately_unescape(link['href']) for link in args[0]['links'] if 'image' in link['type']]
            self.images+=find_images(ultimately_unescape(str(args[1])))
            try:
                self.images+=[media['url'] for media in args[0]['media_content'] if 'image' in media['type']]
            except KeyError:
                pass
            self.images=[image for index, image in enumerate(self.images) if self.images.index(image)==index and image]

    def show_fields(self):
        '''Prints all the fields this object has'''
        print('\n\n'+'Title: '+self.title)
        print('Link: '+self.source)
        print('Date: '+self.date)
        print('\n'+self.content)
        print('\nImages: ')
        for number, image in enumerate(self.images):
            print('['+str(number+1)+'] '+image)


def append_existing(appendee, frame, content):
    """Creates a NewsFeed object with copying its fields from existing objects;
    Appends created object to an existing list of NewsFeed objects
    """
    appendee.append(NewsFeed(None))
    appendee[-1].steal_title(frame)
    appendee[-1].steal_news(content)
    return appendee

def cut_news_off(limit, feed):
    '''Implements logic of --limit argument, also works with a bunch of items from different sources'''
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
    '''Converts pubdate to %Y%m%d format; it is used as a file name for caching'''
    try:
        return datetime.strptime(news.date, '%a, %d %b %Y %H:%M:%S %z').strftime('%Y%m%d')
    except ValueError:
        return datetime.strptime(news.date, '%d %b %Y %H:%M:%S %z').strftime('%Y%m%d')

def find_images(text):
    '''Takes BeautifulSoup representation of a news article as an argument and searches for additional images'''
    logging.info('Searching for additional images...')
    res=[]
    occurences=re.finditer('<img',text)
    tags=[(text.rfind('<',0,item.start()+2),text.find('>',item.start()+2)) for item in occurences]
    where_links_start=[text.find('src',start,end)+5 for start, end in tags]
    borders=[(start,text.find('"',start)) for start in where_links_start]
    res+=[text[opener:closer] for opener, closer in borders]
    return res

def get_all_filenames(news):
    """Takes a NewsFeed object as an argument
    Returns a list of all pubdates mentioned in this news source at a given moment (%Y%m%d format)
    """
    return list(set(date_to_filename(item) for item in news))

def hide(text, starts_with, ends_with):
    '''Gets rid of parts of text that shouldn't be visible (like HTML tags)'''
    return re.sub(re.compile(starts_with+'.*?'+ends_with),'',text)

def insert_cache(cache_files, cache):
    '''Writes newly formed cache to respective files'''
    jsonpickle.set_encoder_options('json', ensure_ascii=False)
    for date, cached_content in zip(cache_files, cache):
        with open('cache/'+date+'.json','w') as cache:
            cache.write(jsonpickle.encode(cached_content))

def make_fb2(news):
    '''Creates an .fb2 file that contains news designed for output'''
    logging.info('Creating an FB2 file...')
    filename=os.path.join(os.path.expanduser('~/Desktop'),datetime.now().strftime('%H%M%S%b%d%Y'))
    with open(filename+'.fb2','w') as filer:
        filer.write('<?xml version="1.0" encoding="UTF-8"?><FictionBook><description></description><body>')
        try:
            for source in news:
                filer.write('<title><p>Source: '+source.title+'</p></title>')
                for item in source.news:
                    filer.write('<title><p>'+item.title+'</p></title>')
                    filer.write('<p>Posted at: '+item.date+'</p>')
                    filer.write('<p>'+item.content+'</p>')
                    filer.write('<p><strong>Source: '+item.source+'</strong></p>')
                    filer.write('<p>Related images: ')
                    for image in item.images:
                        filer.write('<p>'+image+'</p>')
                    filer.write('</p>')
            filer.write('</body></FictionBook>')
        except TypeError:
            for source in news:
                filer.write('<p>'+source+'</p>')
        filer.write('</body></FictionBook>')

def make_json(news):
    '''Converts news to JSON format'''
    logging.info('Converting to JSON...')
    jsonpickle.set_encoder_options('json', ensure_ascii=False)
    return [jsonpickle.encode(item) for item in news]

def make_html(news):
    '''Creates an .html file that contains news designed for output'''
    logging.info('Creating an HTML file...')
    filename=os.path.join(os.path.expanduser('~/Desktop'),datetime.now().strftime('%H%M%S%b%d%Y'))
    with open(filename+'.html','w') as filer:
        filer.write('<html>\n<head></head><body>')
        try:
            for source in news:
                filer.write('<div style="margin-bottom: 75px"><h2>'+source.title+'</h2><div style="margin-left: 75px">')
                for item in source.news:
                    filer.write('<h4>'+item.title+'</h4>')
                    filer.write('Posted at '+item.date)
                    filer.write('<br><br><p>'+item.content+'</p>')
                    filer.write('<p><a href="'+item.source+'">Source</a></p>')
                    for image in item.images:
                        filer.write('<img src="'+image+'">')
                    filer.write('<hr>')
                filer.write('</div></div>')
        except TypeError:
            for source in news:
                filer.write(source)
        filer.write('</body></html>')
    print('All news can be found in '+filename+'.html on your desktop')

def parse_arguments():
    '''Parses arguments from command line'''
    parser=argparse.ArgumentParser(description='Pure Python command-line RSS reader.')
    exclusive=parser.add_mutually_exclusive_group()
    parser.add_argument('--json',action='store_true', help='Print result as JSON in stdout')
    parser.add_argument('--verbose',action='store_true',help='Outputs verbose status messages')
    parser.add_argument('--limit', type=int,action='store',help='Limit news topics if this parameter provided')
    parser.add_argument('--to-html', action='store_true',help='Creates an .html file with news designed to be printed')
    parser.add_argument('--to-fb2', action='store_true', help='Creates an .fb2 file with news designed to be printed')
    exclusive.add_argument('--version',action='store_true',help='Print version info')
    exclusive.add_argument('source',nargs='?',help='RSS URL',default=None)
    exclusive.add_argument('--date', type=str, action='store', help='Print news posted at a certain date')
    return parser.parse_args()

def print_news(news):
    '''Prints any content that's designed to be printed'''
    try:
        for source in news:
            print('\nSource: '+source.title)
            for item in source.news:
                item.show_fields()
    except TypeError:
        print(list(map(lambda x: hide(x,'"py/object":','", '), news)))

def retrieve_cached_news(filenames):
    '''Reads cache from all files mentioned in filenames'''
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
    '''Unescapes HTML characters multiple times (turned out to be an issue with some sources)'''
    logging.info('Unescaping HTML characters...')
    while html.unescape(text)!=text:
        text=html.unescape(text)
    return text

def update_cache(fresh_news, dates, cached):
    '''Appends retrieved news to existing cache'''
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
            cached_content=append_existing(cached_content, fresh_news[0], news_to_append)
    return cached
               
def main():
    args=parse_arguments()
    if args.version and (args.json or args.limit or args.topdf):
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
        feed=cut_news_off(args.limit, feed)
        if args.json:
            feed=make_json(feed)
        if args.to_html:
            make_html(feed)
        if args.to_fb2:
            make_fb2(feed)
        print_news(feed)

if __name__=='__main__':
    main()
