import feedparser
import argparse
import json
import requests
import datetime
import base64
"""import section"""


version = 0.1
parser = argparse.ArgumentParser()
parser.add_argument("URL", help="This is the full adress of the rss feed.use ' ' ")
parser.add_argument("-l", "--lim", help="outputs the latest X articles. can be run without lim to get all articles")
parser.add_argument("-o", "--output", help="outputs news to file", action="store_true")
parser.add_argument("-j", "--json", help="outputs a jsonDump", action="store_true")
parser.add_argument("-d", "--dl", help="downloads data.makes a file as date right now", action="store_true")
parser.add_argument("-r", help="reads the dl version of the feed. arg is the date of dl, you dont need a working url")
#parser.add_argument("--pdf", help="converts the output to the specified format (.pdf) ")
#parser.add_argument("--html", help="converts the output to the specified format (.html) ")
args = parser.parse_args()
limit = args.lim


def captureFeed(URL):
    """Gets a feed fo everything to use"""
    feed = feedparser.parse(args.URL)
    return feed


def fileOutput():
    """Outputs a json dump of feed.entries to a file that is called "news.txt".works """
    open("news.txt", "w").close()
    feed = captureFeed(args.URL)
    f = open("news.txt", "w+")
    input1 = json.dumps(feed.entries)
    f.write(input1)
    f.close()


def standardOutput():
    """This is what happens when there are no tail commands added"""
    if not args.r:
        feed = captureFeed(args.URL)
    else:
        remoteFeed = remoteRead()
        feed = remoteFeed
    for article in feed.entries:
        print("Title:  ", article.title.replace("&#39;", "'"), "\nDate:   ",
              article.published, "\nLinks:  ", article.link, "\n")

def jsonOutput():
    """Outputs a json Dump to the console"""
    feed = captureFeed(args.URL)
    print(json.dumps(feed.entries))


def limitedOutput(limit):
    if not args.r:
        feed = captureFeed(args.URL)
    else:
        remoteFeed = remoteRead()
        feed = remoteFeed
    try:
        for Index in range(int(limit)):
            T = str(feed.entries[Index].title)
            P = feed.entries[Index].published
            L = feed.entries[Index].link
            print("Title:  ", T.replace("&#39;", "'"), "\nDate:   ",
                  P, "\nLinks:  ", L, "\n")
        print("your limit was: ", limit)
    except IndexError:
        print("no")
    """Output if the user uses the --limit args, protected by indexError"""


def cacheDate(URL):
    response = requests.get(URL)
    today = datetime.date.today()
    dateNow = today.strftime("%d-%m-%Y")
    filename = dateNow + ".xml"
    with open(filename, 'wb') as file:
        file.write(response.content)


def remoteRead():
    remoteFeed = feedparser.parse(args.r)
    return remoteFeed


def getPics():
    feed = captureFeed(args.URL)
    listOfPics = []
    try:
        for i in range(len(feed.entries)-1):
            pics = feed.entries[i].media_content[0].get('url')
            listOfPics.append(pics)
    except IndexError:
        print("not all posts have images")
    print(listOfPics)

getPics()        
if limit and not args.r:
    limitedOutput(limit)
elif args.json:
    jsonOutput()
elif not limit and not args.r:
    standardOutput()

if args.r and not limit:
    remoteRead()
if limit and args.r:
    limitedOutput(limit)


if args.dl:
    cacheDate(args.URL)



if args.output:
    feed = captureFeed(args.URL)
    fileOutput()
    """Has to go away from the global score. could try to put it into a main()"""
