import argparse
import requests

parser = argparse.ArgumentParser(description='Pure Python command-line RSS reader.', prog='rss_reader')
parser.add_argument("source", type=str, nargs='?', default=None, help="RSS URL")
parser.add_argument('--version', help="print version info", action='version', version='%(prog)s 1.1')
parser.add_argument("--json", help="print result as JSON in stdout", action="store_true")
parser.add_argument("--verbose", help="outputs verbose status messages", action="store_true")
parser.add_argument("--limit", type=int, help="limit news topics if this parameter provided")
args = parser.parse_args()

if args.source != None:
    print(requests.get(args.source).text)
