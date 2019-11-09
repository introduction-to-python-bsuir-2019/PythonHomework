import argparse

parser = argparse.ArgumentParser(description='Pure Python command-line RSS reader.')
parser.add_argument(
    'source',
    action='store',
    type=str,
    help='RSS URL'
)
parser.add_argument(
    '--version',
    action='version',
    version='%(prog)s'+' 0.0.1',
    help='Print version info'
)
parser.add_argument(
    '--json',
    help='Print result as JSON in stdout',
    action='store_true'
)
parser.add_argument(
    '--verbose',
    help='Outputs verbose status messages',
    action='store_true'
)
parser.add_argument(
    '--limit',
    type=int,
    action='store',
    default=1,
    help='Limit news topics if this parameter provided'
)
print(parser.parse_args().limit)
