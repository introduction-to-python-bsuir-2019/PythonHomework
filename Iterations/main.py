import argparse
from rss_reader import RSSReader


def print_to_console(channel_title, feeds):
    print()
    print('Feed:', channel_title)
    print('-' * 40)
    for item in feeds:
        print('Title:', item['title'])
        print('Date:', item['date'])
        print('Link:', item['link'])
        print()
        print('Image title:', item['image_title'])
        print('Image description:', item['image_description'])
        print('Image link:', item['image_link'])
        print('-' * 40)


def main():
    parser = argparse.ArgumentParser(description='Pure Python command-line RSS reader.')
    parser.add_argument('source', type=str, help='RSS URL')
    parser.add_argument('--limit', type=int, help='Limit news topics if this parameter provided')

    args = parser.parse_args()

    reader = RSSReader(**vars(args))
    channel_title, feeds = reader.parse_source()
    print_to_console(channel_title, feeds)


if __name__ == '__main__':
    main()
