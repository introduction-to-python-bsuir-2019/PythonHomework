import argparse
import feedparser
import logging
import html
import json
from pathlib import Path
from bs4 import BeautifulSoup
# from rss_reader import version as vers
import version as vers


class NewsFeed:
    """Base class for news feed"""
    def __init__(self, feed_title, items):
        self.feed_title = feed_title
        self.items = items

    def print_to_json(self, limit):
        logging.info('Printing news in json format')
        print(json.dumps(self.create_json(0, limit)))

    def create_json(self, is_cached, limit):
        return {'Feed': self.feed_title, 'Items': [item.return_item(is_cached) for item in self.items[:limit]]}

    def print_to_console(self, limit):
        logging.info('Printing news in console format')
        print('Feed: {0}'.format(self.feed_title))
        for item in self.items[:limit]:
            item.print_to_console()
        logging.info('Printed %s news', limit)

    def print_feed(self, json, limit):
        if limit > len(self.items) or limit < 0:
            limit = len(self.items)
        if(json):
            self.print_to_json(limit)
        else:
            self.print_to_console(limit)

    def save_news(self, limit):
        logging.info('Saving news')
        news_to_save = self.create_json(1, limit)['Items']
        existing_news = load_from_cache()
        news_to_save += [item for item in existing_news if not item in news_to_save]
        with open('cache.json', 'w') as json_file:
            json.dump(news_to_save, json_file)


class Item:
    """
    Class for single news item from news feed
    Attributes of the class are:
        title          a
        pubDate        a
        link           a
        description    a
        links          a
        date_string    a
        source         a
    """
    def __init__(self, news_dict):
        for key in news_dict:
            setattr(self, key, news_dict[key])


    def print_to_console(self):
        print('\nTitle: {0}'.format(self.title))
        print('Date: {0}'.format(self.pubDate))
        print('Link: {0} \n'.format(self.link))
        print(self.description)
        print()

        if self.links['href_links']:
            print('\nLinks:')
            for link in self.links['href_links']:
                print(link)

        if self.links['images_links']:
            print('\nImages:')
            for link in self.links['images_links']:
                print(link)

        if self.links['video_links']:
            print('\nVideos:')
            for link in self.links['video_links']:
                print(link)
        print('\n//////////////////////////////////////////////////////////////////////////')

    def return_item(self, is_cached):
        item_content = {'title': self.title, 'description': self.description,
                        'link': self.link, 'pubDate': self.pubDate, 'links': self.links}
        if is_cached:
            item_content['date_string'] = self.date_string
            item_content['source'] = self.source

        return item_content


def set_argparse():
    parser = argparse.ArgumentParser(description='Pure Python command-line RSS reader.')
    parser.add_argument('source', type=str, help='RSS URL')

    parser.add_argument('--version', action='version', version='%(prog)s v'+vers.__version__, help='Print version info')
    parser.add_argument('--json', action='store_true', help='Print result as JSON in stdout')
    parser.add_argument('--verbose', action='store_true', help='Outputs verbose status messages')
    parser.add_argument('--limit', type=int, default=-1, help='Limit news topics if this parameter provided')
    parser.add_argument('--date', type=str, help='Shows news of specific date')
    return parser.parse_args()


def find_images(args, soup):
    logging.info('Starting image finding')
    image_iterator = 0
    images_links = []
    for img in soup.findAll('img'):

        image_iterator += 1
        if 'alt' in img.attrs and img['alt'] != '':
            replaced_data = ' [image {0} | {1}] '.format(image_iterator, img['alt'])
        else:
            replaced_data = ' [image {0}]'.format(image_iterator)
        src = img['src']
        images_links.append('[{0}]: {1}'.format(image_iterator, src))
        soup.find('img').replace_with(replaced_data)

    logging.info('Image finding finished. Found %s images', image_iterator)
    return images_links


def find_href(args, soup):
    logging.info('Starting link finding')
    href_iterator = 0
    href_links = []
    for href in soup.findAll('a'):

        if 'href' in href.attrs:
            href_iterator += 1
            link = href['href']
            if href.text != '':
                replaced_data = ' [link {0} | {1}] '.format(href_iterator, href.text)
            else:
                replaced_data = ' [link {0}] '.format(href_iterator)
            href_links.append('[{0}]: {1}'.format(href_iterator, link))
            soup.find('a').replace_with(replaced_data)
    logging.info('Link finding finished. Found %s links', href_iterator)
    return href_links


def find_videos(args, soup):
    logging.info('Starting video finding')
    video_iterator = 0
    video_links = []
    for video in soup.findAll('iframe'):
        if 'src' in video.attrs:
            video_iterator += 1
            link = video['src']
            replaced_data = ' [video {0}] '.format(video_iterator)
            video_links.append('[{0}]: {1}'.format(video_iterator, link))
            soup.find('iframe').replace_with(final)
    logging.info('Video finding finished. Found %s videos', video_iterator)
    return video_links


def read_from_cache(date, source):
    cached_news = load_from_cache()
    dated_news = []
    for news in cached_news:
        if news['source'] == source and news['date_string'] == date:
            dated_news.append(Item(news))
    return dated_news


def load_from_cache():
    logging.info('Loading from cache')
    cached_news = []
    if Path('cache.json').is_file():
        with open("cache.json") as cache:
            data = cache.read()
            cached_news = json.loads(data)
    logging.info('Loaded %s news', len(cached_news))
    return cached_news


def main():
    try:
        args = set_argparse()
        if args.verbose:
            logging.basicConfig(format='%(asctime)s %(funcName)s %(message)s', datefmt='%I:%M:%S', level=logging.DEBUG)

        logging.info('Application started. RSS source is %s', args.source)
        args.source = args.source.rstrip('/')

        if args.date:
            news = read_from_cache(args.date, args.source)
            if not news:
                raise Exception('The are no news of {0} from {1} stored'.format(args.source, args.date))
            news_feed = NewsFeed('Cached news', news)
        else:
            parsed_feed = feedparser.parse(args.source)
            if parsed_feed.bozo == 1:
                raise Exception('The feed is not well-formed XML. Details are {0}'.format(parsed_feed.bozo_exception))
            # if 'status' not in NewsFeed:
            #    raise Exception('An error happened such that the feed does not contain an HTTP response')
            news = []
            logging.info('Begin processing each news')
            for i in range(len(parsed_feed.entries)):
                logging.info('Parsing news number %s', i + 1)
                entry = parsed_feed.entries[i]
                soup = html.unescape(BeautifulSoup(entry['summary'], 'html.parser'))
                images_links = find_images(args, soup)
                href_links = find_href(args, soup)
                video_links = find_videos(args, soup)
                links = {'images_links': images_links, 'href_links': href_links, 'video_links': video_links}
                date_string = ''.join(map(str, entry.published_parsed[:3]))
                dict_news = {'title': html.unescape(entry['title']), 'pubDate': entry['published'], 'link': entry['link'],
                             'description': html.unescape(soup.text), 'links': links, 'date_string': date_string,
                             'source': args.source}
                news.append(Item(dict_news))
                logging.info('News number %s has parsed', i + 1)
            news_feed = NewsFeed(parsed_feed.feed.title, news)
            news_feed.save_news(len(parsed_feed.entries))
        news_feed.print_feed(args.json, args.limit)

        logging.info('Application completed')

    except Exception as e:
        print(e)


if __name__ == '__main__':

    main()
