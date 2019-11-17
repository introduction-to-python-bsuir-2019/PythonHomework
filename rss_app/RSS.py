import feedparser
from bs4 import BeautifulSoup
import json


class RssAggregator():
    feedurl = ""

    def __init__(self, args, log):
        self.args=args
        self.log=log

    def get_news(self):
        self.log.info("Getting rss feed")
        thefeed = feedparser.parse(self.args.source)      
        return thefeed.entries[:self.args.limit]        

    def print_news(self, entries):
        self.log.info("Printing news")      
        for thefeedentry in entries:
            print("--------------------------------------------------")        
            print("Title: ", thefeedentry.title)
            print("Date: ", thefeedentry.published)
            print("Link: ", thefeedentry.link)
            print(BeautifulSoup(thefeedentry.description, "html.parser").text)  

    def print_json(self, entries):
        self.log.info("RSS feed to json")
        for thefeedentry in entries:
            news={
                "Title": thefeedentry.title,
                "Date": thefeedentry.published,
                "Link": thefeedentry.link,
                "Discription": BeautifulSoup(thefeedentry.description, "html.parser").text
            }
            print("--------------------------------------------------") 
            print(json.dumps(news, indent=3))

            