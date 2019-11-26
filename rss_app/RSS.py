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

    def save_to_json_file(self,entries):
        self.log.info("Save feed to json file")
        news_list = list()
        file_name = self.get_file_name()
        with open(file_name, "w") as write_file:
            for thefeedentry in entries:
                news={
                    "Title": thefeedentry.title,
                    "Date": thefeedentry.published,
                    "Link": thefeedentry.link,
                    "Discription": BeautifulSoup(thefeedentry.description, "html.parser").text
                }
                news_list.append(news)
            json.dump(news_list, write_file, indent=3)

    def get_file_name(self):
        file_name_list = self.args.source.split("//")
        file_name = file_name_list[1].replace("/", "")
        file_name += ".json"
        return file_name

    def get_from_json_file(self):
        file_name = self.get_file_name()
        try:
            with open(file_name, "r") as read_file:
                news = json.load(read_file)
        except FileNotFoundError:  
            print("Error") 
        return news

            