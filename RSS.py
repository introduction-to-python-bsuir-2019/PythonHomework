import feedparser


class RssAggregator():
    feedurl = ""

    def __init__(self, paramrssurl):
        print("links: ", paramrssurl)
        self.feedurl = paramrssurl
        self.parse()

    def parse(self):
        thefeed = feedparser.parse(self.feedurl)
      
        print('Number of RSS posts :', len(thefeed.entries))

        print("Feed: ", thefeed.feed.get("title", ""))
      
        for thefeedentry in thefeed.entries:
            print("--------------------------------------------------")        
            print("Title: ", thefeedentry.get("title", ""))
            print("Date: ", thefeedentry.get("published",""))
            print("Link: ", thefeedentry.get("link", ""))
            print(thefeedentry.get("description", ""))
            
            
        
