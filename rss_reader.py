import argparse
import requests
import html
from bs4 import BeautifulSoup
import re
import json
import feedparser

parser=argparse.ArgumentParser(description='Pure Python command-line RSS reader.')
exclusive=parser.add_mutually_exclusive_group()
parser.add_argument('--json',action='store_true', help='Print result as JSON in stdout')
parser.add_argument('--verbose',action='store_true',help='Outputs verbose status messages')
parser.add_argument('--limit', type=int,action='store',help='Limit news topics if this parameter provided')
exclusive.add_argument('--version',action='store_true',help='Print version info')
exclusive.add_argument('source',nargs='?',help='RSS URL',default=None)
args=parser.parse_args()


version='v1.1'
err={1: 'You don\'t use --version together with other arguments',
    2: 'Source or --version expected',
    3: 'Incorrect limit input (likely to be non-positive input)'}


class Error(Exception):
    def __init__(self, code):
        self.error=code


class News:
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


def verboser(func,action):
    def wrapper(*args, **kwargs):
        print('Started '+action)
        result=func(*args,**kwargs)
        print('Finished '+action)
        return result
    return wrapper

def ultimately_unescape(text):
    while html.unescape(text)!=text:
        text=html.unescape(text)
    return text

def find_images(text):
    res=[]
    occurences=re.finditer('<img',text)
    tags=[(text.rfind('<',0,item.start()+2),text.find('>',item.start()+2)) for item in occurences]
    where_links_start=[text.find('src',start,end)+5 for start, end in tags]
    borders=[(start,text.find('"',start)) for start in where_links_start]
    res+=[text[opener:closer] for opener, closer in borders]
    return res

def clear_tags(text):
    while text.find('<')>-1 and text.find('>')>-1:
        text=text.replace(text[text.find('<'):text.find('>')+1],'')
    return text

def retrieve_news(link, limit):
    feed=feedparser.parse(link)
    soup=requests.get(link).text
    soup=BeautifulSoup(soup,"html5lib")
    news_separated=soup('item')
    print('\nSource: '+feed['feed']['title'])
    newsdict=feed['entries']
    news=[]
    for index, item in (enumerate(newsdict[:min(limit,len(newsdict))]) if limit else enumerate(newsdict)):
        news.append(News(item,news_separated[index]))
    return news


def make_json(news):
    with open('news.json','w') as filer:
        for item in news:
            json.dump(item.__dict__,filer)

def print_news(news):
    for item in news:
        item.show_fields()

if args.version and (args.json or args.limit):
    raise Error(err[1])
if not (args.version or args.source):
    raise Error(err[2])
if args.limit and args.limit<1:
    raise Error(err[3])

if args.version:
    print('RSS-reader '+version)
else:
    if args.verbose:
        print_news=verboser(print_news,'printing')
        retrieve_news=verboser(retrieve_news,'retrieving')
        make_json=verboser(make_json,'making JSON')
    news=retrieve_news(args.source,args.limit)
    print_news(news)
    if args.json:
        make_json(news)

