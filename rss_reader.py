import argparse
import requests
import html
from bs4 import BeautifulSoup

parser=argparse.ArgumentParser(description='Pure Python command-line RSS reader.')
parser.add_argument('source',nargs='?',help='RSS URL')
parser.add_argument('--version',action='store_true',help='Print version info')
parser.add_argument('--json',action='store_true', help='Print result as JSON in stdout')
parser.add_argument('--verbose',action='store_true',help='Outputs verbose status messages')
parser.add_argument('--limit', type=int,action='store',help='Limit news topics if this parameter provided')
args=parser.parse_args()

version='v1.0'
err={1: 'You don\'t use --version together with other arguments',
    2: 'Source or --version expected',
    3: 'Incorrect limit input'}


class Error(Exception):
    def __init__(self, code):
        self.error=code


class News:
    def __init__(self,wall_of_text):
        self.title=convert_to_readable_head(wall_of_text,'title')
        self.source=convert_to_readable_body(wall_of_text,'a href=')
        self.date=convert_to_readable_head(wall_of_text,'pubdate')
        self.content=convert_to_readable_body(wall_of_text,'</a')
        self.images=convert_to_readable_body(wall_of_text,'img src=')

    def show_fields(self):
        print('\n\n\n'+'Title: '+self.title)
        print('Link: '+self.source)
        print('Date: '+self.date)
        print('\n'+self.content)
        print('\nImage: '+self.images)


def verboser(func,action):
    def wrapper(*args, **kwargs):
        print('Started '+action)
        result=func(*args,**kwargs)
        print('Finished '+action)
        return result
    return wrapper

def ultimately_unescape(str):
    while html.unescape(str)!=str:
        str=html.unescape(str)
    return str

def convert_to_readable_head(text,tag_name):
    readable=text(tag_name)[0]
    readable=str(readable)[len(tag_name)+2:-len(tag_name)-3]
    return ultimately_unescape(readable)

def convert_to_readable_body(text,tag_name):
    body=convert_to_readable_head(text,'description')
    body=str(body)
    cutfrom=body.find(tag_name)+len(tag_name)+1
    return body[cutfrom:min(body.find('"',cutfrom),body.find('<',cutfrom))]
    

def retrieve_news(link, limit):
    soup=requests.get(link).text
    soup=BeautifulSoup(soup,"html5lib")
    title=convert_to_readable_head(soup,'title')
    print('Source: '+title)
    content=soup('item')
    news=[]
    for item in (content[:min(limit,len(content))] if limit else content):
        news.append(News(item))
    return news


def make_json(*args):
    pass

def print_news(news):
    for item in news:
        item.show_fields()


if args.version and (args.source or args.json or args.verbose or args.limit):
    raise Error(err[1])
if not (args.version or args.source):
    raise Error(err[2])
if args.limit and args.limit<1:
    raise Error(err[3])

if args.version:
    print('Current version of RSS-reader: '+version)
else:
    if args.verbose:
        print_news=verboser(print_news,'printing')
        retrieve_news=verboser(retrieve_news,'retrieving')
        make_json=verboser(make_json,'making JSON')
    news=retrieve_news(args.source,args.limit)
    print_news(news)
    if args.json:
        make_json(news)

