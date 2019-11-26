from bs4 import BeautifulSoup as BSoup
from urllib.request import Request
from urllib.request import urlopen
import re
import logging
import json
from rss_reader import argparser, get_rss

""" List of selected data"""
args = argparser()
soup = BSoup(get_rss(args.source), "xml")
title = []
date = []
description = []
link = []
image_link = []


def get_title(item):
    """Getting Title"""
    titles = item.find('title').string
    title.append(titles.replace("&#39;", "'").replace("&quot;", ""))
    logging.info('Get title success')


def get_date(item):
    """Getting Date"""
    date.append(item.find('pubDate').string)
    logging.info('Get date success')


def get_description(item):
    """Getting Description"""
    descript = item.find('description').string
    descript = descript.replace("&#39;", "'").replace("&quot;", "").replace("&gt;", "").replace("&nbsp;&nbsp;", "\n")
    """Formatting Description Text"""
    description.append(re.sub('<.*?>', '', descript))
    logging.info('Get description success')


def get_link(item):
    """Getting Link"""
    link.append(item.find('link').string)
    logging.info('Get link source success')
    media_link = item.find_all('media:content')
    images = []  # List of image links for one item
    for img_link in media_link:
        if (img_link.get('type') == 'image/jpeg') or (not img_link.get('type')):
            images.append(img_link.get('url'))
    image_link.append(images)
    logging.info('Get image link success')


def get_feed():
    """Getting Feed """
    logging.info("Limit is: (%s) " % str(args.limit))
    logging.info("Find <item> tags in feed.")
    items = soup.find_all('item', limit=args.limit)
    for item in items:
        get_link(item)
        get_date(item)
        get_description(item)
        get_title(item)
    else:
        logging.info("All goods:)")


def print_news():
    """Outputs News"""
    feed = soup.title.string
    print("\nFeed: " + feed + "\n")
    for number in range(0, len(title)):
        print('Title: ' + title[number])
        print('Date: ' + date[number])
        print('Link: ' + link[number])
        print('\nNews: ' + description[number])
        if image_link[number]:
            print('\nImage link: ')
            print('\n'.join(image_link[number]))
            print('\n\n')
        else:
            logging.info(' Feed #' + str(number) + ' doesn\'t has image')
            print('\nImage link: None\n\n')
    logging.info("All news are printed")


def get_news():
    """Getting News"""
    logging.info("Start parsing feeds")
    get_feed()
    feed_data = soup.title.string
    print("\nFeed: " + feed_data + "\n")
    print_news()


def json():
    print(json.dumps({'title': soup.find('title').string,
                      'news': [{'Title': title[number],
                                'Date': date[number],
                                'Link': link[number],
                                'Feed': description[number],
                                'Image link': image_link[number]
                                } for number in range(0, len(title))]}, ensure_ascii=False, indent=4))


def main():
    open('logger.log', 'w').close()
    if argparser().verbose:
        logging.basicConfig(format=u'%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s',
                            level=logging.DEBUG,
                            filename='logger.log')


get_news()

if __name__ == '__main__':
    main()
