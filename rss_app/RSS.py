import feedparser
from bs4 import BeautifulSoup
import json
from dateutil.parser import parse
import urllib
import httplib2
import os


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
            try:
                print("--------------------------------------------------")        
                print("Title: ", thefeedentry.title)
                print("Date: ", thefeedentry.published, end="\n\n")                    
                print("Alt image: ", BeautifulSoup(thefeedentry.description, "html.parser").find('img')['alt'])
                print(BeautifulSoup(thefeedentry.description, "html.parser").text, end="\n\n")
                print("Links:")
                print("News: ", thefeedentry.link)
                print("Image: ", BeautifulSoup(thefeedentry.description, "html.parser").find('img')['src'])
            except TypeError:
                self.log.info("TypeError: 'NoneType'")

    def print_json(self, entries):
        self.log.info("RSS news to json")
        for thefeedentry in entries:
            try:
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
            except TypeError:
                self.log.info("TypeError: 'NoneType'")

    def save_to_json_file(self,entries):
        self.log.info("Save news to json file")
        news_list = list()
        file_name = self.get_file_name()
        with open(file_name, "w", encoding="utf-8") as write_file:
            for thefeedentry in entries:
                try:
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
                    self.save_image(thefeedentry, file_name)
                    news_list.append(news)
                except TypeError:
                    self.log.info("TypeError: 'NoneType'")                             
            json.dump(news_list, write_file, indent=3)

    def get_file_name(self):
        self.log.info("Getting file name")
        file_name_list = self.args.source.split("//")
        file_name = file_name_list[1].replace("/", "")
        file_name += ".json"
        return file_name

    def save_image(self, thefeedentry, file_name):
        file_path = self.get_path_image(thefeedentry)
        h = httplib2.Http('.cache')
        response, content = h.request(BeautifulSoup(thefeedentry.description, "html.parser").find('img')['src'])      
        try:
            out = open(file_path, "wb")
            out.write(content)
            out.close()
        except FileNotFoundError:
            print("Error")      

    def get_path_image(self, thefeedentry):
        self.log.info("Getting image name")
        file_name_list = self.args.source.split("//")
        file_name = file_name_list[1].replace("/", "")
        folder_path = "image_" + file_name + os.path.sep
        if not os.path.exists(folder_path):
            self.log.info('Creating directory images')
            os.mkdir(folder_path)        
        img = BeautifulSoup(thefeedentry.description, "html.parser").find('img')['src']
        image = img.split("/")
        file_path = os.path.abspath('') + os.path.sep + folder_path + image[-1]
        if ".jpg" or ".gif" or ".png" in file_path:
            return file_path
        file_path += ".jpg"
        return file_path

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

    def get_news_for_converter(self):
        self.log.info("Getting news for converter")
        file_name = self.get_file_name()
        news = list()
        try:
            with open(file_name, "r") as read_file:                          
                news = json.load(read_file)
            return news
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
            