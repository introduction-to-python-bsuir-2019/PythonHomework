import argparse
import logging
import urllib3
from bs4 import BeautifulSoup
import feedparser
import urllib.request
import sys
import json


def making_log(operation, message, file='loglist.log'):
    """func can do 2 ops, if 1 to write if 0 to read"""
    if bool(operation):
        logging.basicConfig(filename=file, format='%(name)s - %(levelname)s - %(message)s-%(asctime)s',
                            level=logging.INFO)
        logging.info(message)
    else:
        print(open(file, 'r').read())


def news_parsing():
    making_log(1, "Opened URL for news reading, URL: %s" % args.source)
    making_log(1, "Limit is: (%s)        " % (str(args.limit)))
    soup = BeautifulSoup(urllib.request.urlopen(args.source), "xml")
    list = soup.find_all("item")
    making_log(1, "Find all <item> tags in feed.")
    print("\n\n\n")
    for cout, feed in enumerate(list):
        if cout != args.limit:
            making_log(1, "Opened feed on %s link." % feed.link.text)
            strmedia = str(feed.find_all("media:content"))
            desc = feed.description.text
            url_list = []
            for i in range(strmedia.count('url="')):
                url_list.append(strmedia[strmedia.find('url="'): (strmedia.find('"', (strmedia.find('url="')+5))+1)])
            if args.json:
                print(json.dumps({"item": {"link": feed.link.text, "body": {"title": feed.title.text,
                                 "date": feed.pubDate.text, "images": str(url_list),
                                 "feed": desc[(desc.find('a>') + 1):desc.find('<p><br')]}}}, indent=4))
            else:
                print("Title: " + feed.title.text,
                      "\nDate: " + feed.pubDate.text,
                      "\nLink: " + feed.link.text)
                print("Feed: " + desc[(desc.find('a>') + 1):desc.find('<p><br')])
                if url_list != []:
                    print("Images: \n\n" + str(url_list))
                print("\n\n\n")
        else:
            making_log(1, "Iteration closed with code 0(all_goods)")
            break

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("source", help="RSS URL", type=str)
    parser.add_argument("--version", action='version', version='%(prog)s ' + 'v 1.2', help="Print version info", )
    parser.add_argument("--json", help="Print result as JSON in stdout", action="store_true")
    parser.add_argument("--verbose", help="Outputs verbose status messages", action="store_true")
    parser.add_argument("--limit", type=int, help="Limit news topics if this parameter provided")
    args = parser.parse_args()
    news_parsing()
    if args.verbose:
        making_log(0, '')


if __name__ == '__main__':
    main()

