import argparse
from functools import reduce

parser=argparse.ArgumentParser(description='Pure Python command-line RSS reader.')
parser.add_argument('source',nargs='?',help='RSS URL')
parser.add_argument('--version',action='store_true',help='Print version info')
parser.add_argument('--json',action='store_true', help='Print result as JSON in stdout')
parser.add_argument('--verbose',action='store_true',help='Outputs verbose status messages')
parser.add_argument('--limit', type=int,action='store',help='Limit news topics if this parameter provided')
args=parser.parse_args()

version='v1.0.1'
err={1: 'Incorrect argument input. Either --version or link are allowed',
    2: 'Incorrect link',}


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


#if args.version==reduce(lambda x,y: x or y,list(map(bool,[args.limit,args.source,args.json,args.verbose]))):
#    raise Error(err[1)



#if args.version:
#    print('Current version of RSS-reader: '+version)
#
#print(args)
#TODO: --limiting
#TODO: --json (limiting included)
#TODO: --verbose
