import feedparser
import argparse
import json

version = 0.1
parser = argparse.ArgumentParser()
parser.add_argument("URL", help="This is the full adress of the rss feed.use ' ' ")
parser.add_argument("-l", "--lim", help="outputs the latest X(int)articles. can be run without lim to get all articles")
parser.add_argument("-o", "--output", help="outputs news to file", action="store_true")
args = parser.parse_args()
limit = args.lim


def captureFeed(url):
    feed = feedparser.parse(args.URL)
    return feed


def fileOutput():
    open("news.txt", "w").close()
    feed = captureFeed(args.URL)
    f = open("news.txt", "w+")
    for n in feed.entries:
        input1 = json.dumps(feed.entries)
        f.write(input1)
    f.close()


def standardOutput():
    """This is what happens when there are no tail commands added"""
    feed = captureFeed(args.URL)
    for article in feed.entries:
        print("Title:  ", article.title.replace("&#39;", "'"), "\nDate:   ",
              article.published, "\nLinks:  ", article.link, "\n")


def limitedOutput(limit):
    """This is what happens when there is only  parameter on limmit"""
    feed = captureFeed(args.URL)
    try:
        for i in range(int(limit)):
            T = str(feed.entries[i].title)
            P = feed.entries[i].published
            L = feed.entries[i].link
            print("Title:  ", T.replace("&#39;", "'"), "\nDate:   ",
                  P, "\nLinks:  ", L, "\n")
        print("your limit was: ", limit)
    except IndexError:
        print("no")


if limit:
    limitedOutput(limit)
else:
    standardOutput()
print(args.output)
if args.output:
    feed = captureFeed(args.URL)
    fileOutput()


"""
I have created the bare minimal working rss reader.
It has 2 parameters other than help. LIMIT and URL.
I will include more as time progresses.
I need to remove logic from the global scope.
I have done most of it but i want to use a class
for this,yet I dont know enough about them yet as I
was ill on the date of the lecture and the powerpoint
was complex for me at this stage
setuptools havent been made yet, Ill try to make them now
"""
