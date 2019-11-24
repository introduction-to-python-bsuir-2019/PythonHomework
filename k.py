import feedparser
import argparse
import json
"""import section"""

version = 0.1
parser = argparse.ArgumentParser()
parser.add_argument("URL", help="This is the full adress of the rss feed.use ' ' ")
parser.add_argument("-l", "--lim", help="outputs the latest X articles. can be run without lim to get all articles")
parser.add_argument("-o", "--output", help="outputs news to file", action="store_true")
parser.add_argument("-j", "--json", help="outputs a jsonDump", action="store_true")
parser.add_argument("-d","-date", help="caches the data and makes a file named by the time right now")
parser.add_argument("-c","--con", help="converts the output to some specified format like .pdf and .html")
args = parser.parse_args()
limit = args.lim
"""ALL MUST GO. I might try to pull an if __main__()"""


def cacheDate():
    print("a")


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
    feed = captureFeed(args.URL)
    for article in feed.entries:
        print("Title:  ", article.title.replace("&#39;", "'"), "\nDate:   ",
              article.published, "\nLinks:  ", article.link, "\n")


def jsonOutput():
    """Outputs a json Dump to the console"""
    feed = captureFeed(args.URL)
    print(json.dumps(feed.entries))


def limitedOutput(limit):
    feed = captureFeed(args.URL)
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


if limit:
    limitedOutput(limit)
elif args.json:
    jsonOutput()
else:
    standardOutput()

if args.output:
    feed = captureFeed(args.URL)
    fileOutput()
    """Has to go away from the global score. could try to put it into a main()"""

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
