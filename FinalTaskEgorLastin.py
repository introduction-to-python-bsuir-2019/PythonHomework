import feedparser
import argparse

def parseRSS( rss_url ):
    return feedparser.parse( rss_url )

def getTimes(rss_url):
    times=[]
    feed=parseRSS(rss_url)
    for newsitem in feed['items']:
        times.append(newsitem['published'])
        return times
    
def getLinks(rss_url):
    links=[]
    feed=  parseRSS(rss_url)
    for newsitem in feed['items']:
        links.append(newsitem[ 'link'])
    return links

#def getTimes( rs_url)
def getHeadlines( rss_url ):
    headlines = []
    feed = parseRSS( rss_url )
    for newsitem in feed['items']:
        headlines.append(newsitem['title'])
    return headlines

# A list to hold all headlines,links,.....

allheadlines=[]
alllinks=[]
alltimes=[]
allpics=[]

# List of RSS feeds that we will fetch and combine
newsurls = {'yahoonews':        'http://news.yahoo.com/rss/'}
# Iterate over the feed urls
for key,url in newsurls.items():
    print(key,url)
    # Call getHeadlines() and combine the returned headlines with allheadlines
    allheadlines.extend( getHeadlines( url ) )
    alllinks.extend( getLinks(url ))
    alltimes.extend( getTimes( url))
    res = "\n".join("Link:    {}\nTitle:       {}\nTime published:        {}\n".format( x, y, z) for  x, y, z in zip(alllinks, allheadlines, alltimes))
# Iterate over the allheadlines list and print each headline
for i in res:
    print(i)
    #print(ln,"\n",hl.replace("&#39;","'"))

#
#
#
"""
import feedparser
import webbrowser
import argparse
parser = argparse.ArgumentParser(description='This is the python-built RSS reader.')
parser.add_argument('-u','--ur',action='store',dest='url',default=None,help='<Required> url link',required=True)
results = parser.parse_args()#output from all of this
feed = feedparser.parse(results.url)
feed_entries = feed.entries

def parseRSS(feed):
    return feedparser.parse(feed)#used
def getHeadlines( results.url ):
    headlines = []
    feed = parseRSS(results.url)
    for newsitem in feed['items']:
        headlines.append(newsitem['title'])

    return headlines

allheadlines = []

for key,url in newsurls.items():
#
    allheadlines.extend(getHeadlines(url))
#
for hl in allheadlines:
    print(hl.replace("&#39;","'"))

def formatEntry(headline,date,link):
	print(1)
"""

