import argparse

parser=argparse.ArgumentParser(description='HIT ME MAN')
parser.add_argument('-v',action='store_true',help='show this help message and exit')
#parser.add_argument('--version',action='store_true',help='Print version info')
#parser.add_argument('--json',action='store_true',help='Print result as JSON in stdout')


args=parser.parse_args()
if args.v:
    print('v')
#if args.version:
#    print('version')
#if args.json:
#    print('json')
