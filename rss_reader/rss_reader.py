import argparse
import feedparser
import logging
import html
import json
from bs4 import BeautifulSoup
# from tqdm import tqdm
from rss_reader import version as vers
# import version as vers


class News_Feed:
    def __init__(self, feed_title, items):
        self.feed_title = feed_title
        self.items = items

    def print_to_json(self):
        logging.info('Printing news in json format')
        print(json.dumps({"Feed": self.feed_title, "Items": [item.return_item() for item in self.items]}))

    def print_to_console(self):
        logging.info('Printing news in console format')
        print('Feed: {0}'.format(self.feed_title))
        for item in self.items:
            item.print_to_console()

    def print_feed(self, json):
        if(json):
            self.print_to_json()
        else:
            self.print_to_console()


class Item:
    def __init__(self, title, date, link, description, links):
        self.title = title
        self.date = date
        self.link = link
        self.description = description
        self.links = links

    def print_to_console(self):
        print('\nTitle: {0}'.format(self.title))
        print('Date: {0}'.format(self.date))
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

    def return_item(self):
        return {"title": self.title, "description": self.description,
                "link": self.link, "pubDate": self.date, "source": self.links}


def set_argparse():
    parser = argparse.ArgumentParser(description='Pure Python command-line RSS reader.')
    parser.add_argument('source', type=str, help='RSS URL')

    parser.add_argument('--version', action='version', version='%(prog)s v'+vers.__version__, help='Print version info')
    parser.add_argument('--json', action='store_true', help='Print result as JSON in stdout')
    parser.add_argument('--verbose', action='store_true', help='Outputs verbose status messages')
    parser.add_argument('--limit', type=int, default=-1, help='Limit news topics if this parameter provided')
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


def main():
    try:
        args = set_argparse()
        if args.verbose:
            logging.basicConfig(format='%(asctime)s %(funcName)s %(message)s', datefmt='%I:%M:%S', level=logging.DEBUG)

        logging.info('Application started. RSS source is %s', args.source)
        NewsFeed = feedparser.parse(args.source)
        if NewsFeed.bozo == 1:
            raise Exception('The feed is not well-formed XML')
        # if 'status' not in NewsFeed:
        #    raise Exception('An error happened such that the feed does not contain an HTTP response')
        if args.limit < 0 or args.limit > len(NewsFeed.entries):
            args.limit = len(NewsFeed.entries)

        news = []
        logging.info('Begin processing each news')
        for i in range(args.limit):
            logging.info('Parsing news number %s', i+1)
            entry = NewsFeed.entries[i]
            soup = html.unescape(BeautifulSoup(entry['summary'], "html.parser"))
            images_links = find_images(args, soup)
            href_links = find_href(args, soup)
            video_links = find_videos(args, soup)
            links = {'images_links': images_links, 'href_links': href_links, 'video_links': video_links}
            news.append(Item(html.unescape(entry['title']), entry['published'], entry['link'], html.unescape(soup.text), links))
            logging.info('News number %s has parsed', i+1)

        newsFeed = News_Feed(NewsFeed.feed.title, news)
        newsFeed.print_feed(args.json)
        logging.info('Application completed')
        
    except Exception as e:
        print(e)
        
if __name__ == '__main__':

    main()
