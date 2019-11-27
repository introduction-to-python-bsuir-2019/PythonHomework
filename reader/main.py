import argparse
from .rss_reader import RSSReader


def main():
    parser = argparse.ArgumentParser(description='Pure Python command-line RSS reader.')
    parser.add_argument('source', type=str, help='RSS URL')
    parser.add_argument('--limit', type=int, help='Limit news topics if this parameter provided')

    args = parser.parse_args()

    reader = RSSReader(**vars(args))
    reader.parse_source()


if __name__ == '__main__':
    main()
