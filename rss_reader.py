import argparse

parser=argparse.ArgumentParser(description='Pure Python command-line RSS reader.')
parser.add_argument('source',help='RSS URL')
parser.add_argument('--version',action='store_true',help='Print version info')
parser.add_argument('--json',action='store_true', help='Print result as JSON in stdout')
parser.add_argument('--verbose',action='store_true',help='Outputs verbose status messages')
parser.add_argument('--limit', type=int,action='store',help='Limit news topics if this parameter provided')

print(parser)


args=parser.parse_args()
