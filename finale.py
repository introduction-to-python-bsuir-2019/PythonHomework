import feedparser
import argparse
import json

version = '1.0'


def print_function(feed, limit, js):
    func_limit = 0
    d = {}

    for entry in feed.entries:
        func_limit += 1
        article_title = entry.title
        article_link = entry.link
        article_date = entry.published
        content = entry.description

        if js == 0:
            print("Title: {}".format(article_title))
            print("Link: [{}]".format(article_link))
            print("Date: {}\n".format(article_date))
            print("Content: [{}]\n\n".format(content))
        else:
            d["Title"] = article_title
            d["Link"] = article_link
            d["Date"] = article_date
            d["Content"] = content
            print(json.dumps(d) + '\n')

        if func_limit == limit:
            break


parser = argparse.ArgumentParser(description='Rss reader programm')
parser.add_argument('link', help='Receive rss url in format: \"url\"')
parser.add_argument('--limit', type=int, default=0, help='Receive int \'x\' and print \'x\' block of news')
parser.add_argument('--version', action='count', default=0, help='Print current version of a program and complete work')
parser.add_argument('--json', action='count', default=0, help="print result as json")

args = parser.parse_args()

feed = feedparser.parse(args.link)
feed_entries = feed.entries

if args.version == 0:
    print_function(feed, args.limit, args.json)
else:
    print("Current version is: ", version)
