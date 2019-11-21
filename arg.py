import argparse

parser = argparse.ArgumentParser(description='Pure python command-line RSS reader')
parser.add_argument("source", help='RSS URL', type=str)
parser.add_argument("--version", action="store_true", help='Print version info')
parser.add_argument("--json", action='store_true', help='Print result as JSON in stdout')
parser.add_argument("--verbose", action='store_true', help='Outputs verbose status messages')
parser.add_argument("--limit", help='Limit news topics', type=int)
parser.add_argument("--date", help='Shows cached news on introduced day', type=int)
args = parser.parse_args()
