import argparse
from .rss_reader import RSSReader


def main():
    parser = argparse.ArgumentParser(description='Pure Python command-line RSS reader.')
    parser.add_argument('source', type=str, help='RSS URL')
    parser.add_argument('--limit', type=int, help='Limit news topics if this parameter provided')
    parser.add_argument('--json', help='Print result as JSON in stdout', action='store_true')
    parser.add_argument('--date', type=str, help='Print news from cache by date')
    parser.add_argument('--to-html', type=str, help='Enter the path where new file will be saved')
    args = parser.parse_args()

    reader = RSSReader(**vars(args))

    reader.parse_source()
