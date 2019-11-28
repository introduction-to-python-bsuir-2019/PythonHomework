import feedparser
from bs4 import BeautifulSoup
import json
from dateutil.parser import parse


class RssAggregator():
    feedurl = ""

    def __init__(self, args, log):
        self.args=args
        self.log=log

    def get_news(self):
        self.log.info("Getting rss feed")
        thefeed = feedparser.parse(self.args.source)
        self.save_to_json_file(thefeed.entries)      
        return thefeed.entries[:self.args.limit]        

    def print_news(self, entries):
        self.log.info("Printing news")      
        for thefeedentry in entries:
            print("--------------------------------------------------")        
            print("Title: ", thefeedentry.title)
            print("Date: ", thefeedentry.published, end="\n\n")                    
            print("Alt image: ", )
            print(BeautifulSoup(thefeedentry.description, "html.parser").text, end="\n\n")
            print("Links:")
            print("News: ", thefeedentry.link)
            print("Image: ", BeautifulSoup(thefeedentry.description, "html.parser").find('img')['src'])

    def print_json(self, entries):
        self.log.info("RSS news to json")
        for thefeedentry in entries:
            news={
                "Title": thefeedentry.title,
                "Date": thefeedentry.published,
                "Alt image": BeautifulSoup(thefeedentry.description, "html.parser").find('img')['alt'],
                "Discription": BeautifulSoup(thefeedentry.description, "html.parser").text,
                "Links":{
                    "News": thefeedentry.link,
                    "Image": BeautifulSoup(thefeedentry.description, "html.parser").find('img')['src']
                }                
            } 
            print(json.dumps(news, indent=3))

    def save_to_json_file(self,entries):
        self.log.info("Save news to json file")
        news_list = list()
        file_name = self.get_file_name()
        with open(file_name, "w") as write_file:
            for thefeedentry in entries:
                news={
                    "Title": thefeedentry.title,
                    "Date": thefeedentry.published,
                    "Alt image": BeautifulSoup(thefeedentry.description, "html.parser").find('img')['alt'],
                    "Discription": BeautifulSoup(thefeedentry.description, "html.parser").text,
                    "Links":{
                        "News": thefeedentry.link,
                        "Image": BeautifulSoup(thefeedentry.description, "html.parser").find('img')['src']
                    }
                }
                news_list.append(news)
            json.dump(news_list, write_file, indent=3)

    def get_file_name(self):
        self.log.info("Getting file name")
        file_name_list = self.args.source.split("//")
        file_name = file_name_list[1].replace("/", "")
        file_name += ".json"
        return file_name

    def get_from_json_file(self):
        self.log.info("Getting news by date")
        file_name = self.get_file_name()
        news_by_date = list()
        try:
            with open(file_name, "r") as read_file:                          
                news = json.load(read_file)
            for thefeedentry in news: 
                published = parse(thefeedentry['Date']).strftime('%Y%m%d')
                if published >= self.args.date:
                    news_by_date.append(thefeedentry)  
            return news_by_date
        except FileNotFoundError:  
            print("File not found error") 
        
    def print_news_from_file(self,entries):
        self.log.info("Printing news by date")        
        for thefeedentry in entries[:self.args.limit]:                  
            print("--------------------------------------------------")       
            print("Title: ", thefeedentry['Title'])
            print("Date: ", thefeedentry['Date'], end="\n\n")
            print("Alt image: ", thefeedentry['Alt image'])                    
            print(thefeedentry['Discription'], end="\n\n")
            print("Links: ")
            print("News: ", thefeedentry['Links']['News'])
            print("Image: ", thefeedentry['Links']['Image'])
            