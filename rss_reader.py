import argparse

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


if bool(args.version)==bool(args.source):
    raise Error(err[1])


#if args.version:
#    print('Current version of RSS-reader: '+version)
#
#print(args)
#TODO: --limiting
#TODO: --json (limiting included)
#TODO: --verbose
