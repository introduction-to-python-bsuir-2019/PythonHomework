import feedparser
import argparse
import json
import datetime
import os

version = '1.0'


def print_function(feed, limit, js):
    func_limit = 0
    d = {}
    now = datetime.datetime.now()
    year = now.year
    month = now.month
    day = now.day
    year_str = str(year)
    if day>9:
        day_str = str(day)
    else:
        day_str = '' + '0' + str(day)
    if month > 9:
        month_str = str(month)
    else:
        month_str = '' + '0' + str(month)
    name = '' + year_str + month_str + day_str + ".txt"
    f = open(name, 'w')

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

        f.write("Title : " + article_title)
        f.write("\nLink: [" + article_link + "]")
        f.write("\nDate: " + article_date)
        f.write("\nContent: [" + content + "]\n\n")

        if func_limit == limit:
            break

    f.close()


def date_function(date):
    name = '' + str(date) + '.txt'
    if os.path.isfile(name):
        f = open(name, 'r')
        for line in f:
            print(line)
        f.close()
    else:
        print("ERROR")


parser = argparse.ArgumentParser(description='Rss reader programm')
parser.add_argument('link', help='Receive rss url in format: \"url\"')
parser.add_argument('--limit', type=int, default=0, help='Receive int \'x\' and print \'x\' block of news')
parser.add_argument('--version', action='count', default=0, help='Print current version of a program and complete work')
parser.add_argument('--json', action='count', default=0, help="print result as json")
parser.add_argument('--date', type=int, default=0, help='Receive yyyymmdd and print news, checked at that day, if they exist')

args = parser.parse_args()

feed = feedparser.parse(args.link)
feed_entries = feed.entries

if args.version != 0:
    print("Current version is: ", version)
else:
    if args.date == 0:
        print_function(feed, args.limit, args.json)
    else:
        date_function(args.date)
