import argparse
import json
import logging
import re
import os

from urllib.request import Request
from urllib.request import urlopen

from bs4 import BeautifulSoup as Soup4


def parsargument():
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
        version='%(prog)s' + ' 0.1',
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
    parser.add_argument(
        '--date',
        type=str,
        action='store',
        nargs=1,
        help='Print news by date. Enter date in format YYYYMMDD'
    )
    return parser.parse_args()


def get_rss(url):
    logging.info('Opened URL for news reading, URL: %s' % url)
    req = Request(url)
    logging.info('Read our request to rss')
    rss = urlopen(req).read()
    return rss


def get_num_date(date: str):
    date = date.split()
    month = {"Jan": "01", "Feb": "02", "Mar": "03", "Apr": "04", "May": "05", "June": "06", "July": "07", "Aug": "08",
             "Sept": "09", "Oct": "10", "Nov": "11", "Dec": "12"}
    return date[3] + month[date[2]] + date[1]


class RssFeed:
    """This class contains lists of title, dates, descriptions,links.
    Methods: get_title, get_date, get_description, get_link, get_feed"""

    def __init__(self):
        """Initialization"""
        self.args = parsargument()  # args contains all arguments
        self.soup = Soup4(get_rss(self.args.source), "xml")  # convert our page to xml
        self.title = []  # List of titles
        self.date = []  # List of dates
        self.description = []  # List of description of feed
        self.link = []  # List of links(not image)
        self.image_link = []  # List of image links

    def get_title(self, item):
        """This method get title of feed"""
        title = item.find('title').string
        self.title.append(title.replace("&#39;", "'").replace("&quot;", ""))
        logging.info('Get title success')

    def get_date(self, item):
        """This method get date of publication"""
        self.date.append(item.find('pubDate').string)
        logging.info('Get date success')

    def get_description(self, item):
        """This method get description of feed"""
        descrip = item.find('description').string
        descrip = descrip.replace("&#39;", "'").replace("&quot;", "").replace("&gt;", "").replace("&nbsp;&nbsp;", "\n")
        self.description.append(re.sub('<.*?>', '', descrip))
        logging.info('Get description success')

    def get_link(self, item):
        """This method get all links from rss"""
        self.link.append(item.find('link').string)
        logging.info('Get link source success')
        media_link = item.find_all('media:content')
        images = []  # List of image links for one item
        for img_link in media_link:
            if (img_link.get('type') == 'image/jpeg') or (not img_link.get('type')):
                images.append(img_link.get('url'))
        self.image_link.append(images)
        logging.info('Get image link success')

    def get_feed(self):
        """This method get all information from rss to string"""
        logging.info("Limit is: (%s) " % str(self.args.limit))
        logging.info("Find <item> tags in feed.")
        items = self.soup.find_all('item', limit=self.args.limit)
        for item in items:
            self.get_link(item)
            self.get_date(item)
            self.get_description(item)
            self.get_title(item)
        else:
            logging.info("All goods:)")

    def print_news(self):
        """This method print feed"""
        right = self.args.source[8:].find('/')
        name = self.args.source[8:right + 8] + '.json'
        if os.path.isfile(name):
            f = open(name, 'r+')
            data = json.load(f)
            for number in range(0, len(self.title)):
                flag = True
                for dates in data['news']:
                    if dates['Date'] == self.date[number]:
                        flag = False
                if flag:
                    data['news'].append({'Title': self.title[number],
                                         'Date': self.date[number],
                                         'Link': self.link[number],
                                         'Feed': self.description[number],
                                         'Image link': self.image_link[number]
                                         })
            f.close()
            f = open(name, 'w')
            f.write(json.dumps(data, indent=4, ensure_ascii=False))
            f.close()
        else:
            f = open(name, 'w')
            newsJson = json.dumps({'title': self.soup.find('title').string,
                                   'news': [{'Title': self.title[number],
                                             'Date': self.date[number],
                                             'Link': self.link[number],
                                             'Feed': self.description[number],
                                             'Image link': self.image_link[number]
                                             } for number in range(0, len(self.title))]}, ensure_ascii=False, indent=4)

            f.write(newsJson)
            f.close()
        if self.args.json:
            print(json.dumps({'title': self.soup.find('title').string,
                              'news': [{'Title': self.title[number],
                                        'Date': self.date[number],
                                        'Link': self.link[number],
                                        'Feed': self.description[number],
                                        'Image link': self.image_link[number]
                                        } for number in range(0, len(self.title))]}, ensure_ascii=False, indent=4))
        else:
            feed = self.soup.title.string
            print("\nFeed: " + feed + "\n")
            for number in range(0, len(self.title)):
                print('Title: ' + self.title[number])
                print('Date: ' + self.date[number])
                print('Link: ' + self.link[number])
                print('\nNews: ' + self.description[number])
                if self.image_link[number]:
                    print('\nImage link: ')
                    print('\n'.join(self.image_link[number]))
                    print('\n\n')
                else:
                    logging.info(' Feed #' + str(number) + ' doesn\'t has image')
                    print('\nImage link: None\n\n')
            logging.info("All news are printed")


def print_date():
    right = parsargument().source[8:].find('/')
    name = parsargument().source[8:right + 8] + '.json'
    logging.info('Get cache news from ' + name)
    logging.info('Check if this file ' + name + ' was create')
    if os.path.isfile(name):
        logging.info(name + ' was create!')
        f = open(name, 'r+')
        data = json.load(f)
        logging.info('Print news from cache file')
        for news in data['news']:
            if get_num_date(news['Date']) == str(parsargument().date[0]):
                print('Title: ' + news['Title'])
                print('Date: ' + news['Date'])
                print('Link: ' + news['Link'])
                print('\nNews: ' + news['Feed'])
                if news['Image link']:
                    print('\nImage link: ')
                    print('\n'.join(news['Image link']))
                    print('\n\n')
                else:
                    print('\nImage link: None\n\n')
        f.close()
    else:
        logging.info(name + 'was not create(')
        print('No cache')


def get_news():
    """This function get information from rss page and print int cmd"""
    logging.info("Start parsing feeds")
    right_length = 8
    if parsargument().date and len(parsargument().date[0]) is not right_length:
        print("Enter date in format %YYYYMMDD")
    if parsargument().date and len(parsargument().date[0]) is right_length:
        print_date()
    else:
        news = RssFeed()
        news.get_feed()
        news.print_news()


def main():
    open('logger.log', 'w').close()
    if parsargument().verbose:
        logging.basicConfig(format=u'%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s',
                            level=logging.DEBUG, filename='logger.log')
    get_news()


if __name__ == '__main__':
    main()
