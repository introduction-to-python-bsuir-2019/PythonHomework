import argparse
import requests
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
    3: 'Entered arguments require source as well'}


class Error(Exception):
    def __init__(self, code):
        self.error=code


def verboser(func,action):
    def wrapper(*args, **kwargs):
        print('Started '+action)
        result=func(*args,**kwargs)
        print('Finished '+action)
        return result
    return wrapper

def retrieve_news(*args):
    pass

def make_json(*args):
    pass


if args.version and (args.source or args.json or args.verbose or args.limit):
    raise Error(err[1])
if not (args.version or args.source):
    raise Error(err[2])

if args.version:
    print('Current version of RSS-reader: '+version)
else:
    if args.verbose:
        retrieve_news=verboser(retrieve_news,'retrieving')
        make_json=verboser(make_json,'making JSON')
    news=retrieve_news(args.source,args.limit)
    if args.json:
        make_json(news)
