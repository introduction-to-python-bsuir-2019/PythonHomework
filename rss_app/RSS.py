"""
A file with the RssAggregator class that parses the URL
and performs various actions with the received data
"""

import feedparser
from bs4 import BeautifulSoup
import json
from dateutil.parser import parse
import urllib
import httplib2
import os
from colorama import init
from colorama import Fore


class RssAggregator():

    """ Class for rss feed """

    feedurl = ""

    def __init__(self, source, limit, date, log, colorize):
        self.source = source
        self.limit = limit
        self.date = date
        self.log = log
        self.colorize = colorize
        init()

    def get_news(self):

        """ Returns parsed news and caches it"""

        self.log.info("Getting rss feed")
        thefeed = feedparser.parse(self.source)
        self.save_to_json_file(thefeed.entries)
        return thefeed.entries[:self.limit]

    def print_news(self, entries):

        """ Print rss news """

        self.log.info("Printing news")
        for thefeedentry in entries:
            try:
                if self.colorize:
                    print("--------------------------------------------------")
                    print(f"{Fore.RED}Title:{Fore.RESET} ", Fore.RED + thefeedentry.title + Fore.RESET)
                    print(f"{Fore.BLUE}Date:{Fore.RESET} ", Fore.BLUE + thefeedentry.published + Fore.RESET, end="\n\n")
                    print(f"{Fore.YELLOW}Alt image:{Fore.RESET} ", Fore.YELLOW + BeautifulSoup(thefeedentry.description + Fore.RESET, "html.parser").find('img')['alt'])
                    print(Fore.GREEN + BeautifulSoup(thefeedentry.description, "html.parser").text + Fore.RESET, end="\n\n")
                    print("Links:")
                    print(f"{Fore.YELLOW}News:{Fore.RESET} ", Fore.YELLOW + thefeedentry.link + Fore.RESET)
                    print(f"{Fore.YELLOW}Image:{Fore.RESET} ", Fore.YELLOW + BeautifulSoup(thefeedentry.description + Fore.RESET, "html.parser").find('img')['src'])
                else:
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

        """ Print rss news in json format"""

        self.log.info("RSS news to json")
        for thefeedentry in entries:
            try:
                news = {
                    "Title": thefeedentry.title,
                    "Date": thefeedentry.published,
                    "Alt image": BeautifulSoup(thefeedentry.description, "html.parser").find('img')['alt'],
                    "Discription": BeautifulSoup(thefeedentry.description, "html.parser").text,
                    "Links": {
                        "News": thefeedentry.link,
                        "Image": BeautifulSoup(thefeedentry.description, "html.parser").find('img')['src']
                    }
                }
                print(json.dumps(news, indent=3))
            except TypeError:
                self.log.info("TypeError: 'NoneType'")

    def save_to_json_file(self, entries):

        """ Save rss news to json file"""

        self.log.info("Save news to json file")
        news_list = list()
        file_name = self.get_file_name()
        with open(file_name, "w", encoding="utf-8") as write_file:
            for thefeedentry in entries:
                try:
                    news = {
                        "Title": thefeedentry.title,
                        "Date": thefeedentry.published,
                        "Alt image": BeautifulSoup(thefeedentry.description, "html.parser").find('img')['alt'],
                        "Discription": BeautifulSoup(thefeedentry.description, "html.parser").text,
                        "Links": {
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

        """ Getting the file name for storing news """

        self.log.info("Getting file name")
        file_name_list = self.source.split("//")
        file_name = file_name_list[1].replace("/", "")
        file_name += ".json"
        return file_name

    def save_image(self, thefeedentry, file_name):

        """ Save image to file"""
   
        file_path = self.get_path_image(thefeedentry)
        h = httplib2.Http('.cache')
        response, content = h.request(BeautifulSoup(thefeedentry.description, "html.parser").find('img')['src'])
        try:
            out = open(file_path, "wb")
            out.write(content)
            out.close()
        except FileNotFoundError:
            self.log.info("Error: image not found")
        except OSError:
            self.log.info("[Errno 22] Invalid argument {}".format(file_path))

    def get_path_image(self, thefeedentry):

        """ Get path image """

        file_name_list = self.source.split("//")
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

        """ Get news on the argument --date from json file"""

        self.log.info("Getting news by date")
        file_name = self.get_file_name()
        news_by_date = list()
        try:
            with open(file_name, "r") as read_file:
                news = json.load(read_file)
            for thefeedentry in news:
                published = parse(thefeedentry['Date']).strftime('%Y%m%d')
                if published >= self.date:
                    news_by_date.append(thefeedentry)
            return news_by_date
        except FileNotFoundError:
            self.log.info("File not found error")

    def get_news_for_converter(self):

        """ Get news from json file for converter in pdf or html"""

        self.log.info("Getting news for converter")
        file_name = self.get_file_name()
        news = list()
        try:
            with open(file_name, "r") as read_file:
                news = json.load(read_file)
            return news
        except FileNotFoundError:
            self.log.info("File not found error")

    def print_news_from_file(self, entries):

        """ Print a certain amount of news by date """

        self.log.info("Printing news by date")
        for thefeedentry in entries[:self.limit]:
            if self.colorize:
                print("--------------------------------------------------")
                print(f"{Fore.RED}Title:{Fore.RESET} ", Fore.RED + thefeedentry['Title'] + Fore.RESET)
                print(f"{Fore.BLUE}Date:{Fore.RESET} ", Fore.BLUE + thefeedentry['Date'] + Fore.RESET, end="\n\n")
                print(f"{Fore.YELLOW}Alt image:{Fore.RESET} ", Fore.YELLOW + thefeedentry['Alt image'] + Fore.RESET)
                print(Fore.GREEN + thefeedentry['Discription'] + Fore.RESET, end="\n\n")
                print("Links: ")
                print(f"{Fore.YELLOW}News:{Fore.RESET} ", Fore.YELLOW + thefeedentry['Links']['News'] + Fore.RESET)
                print(f"{Fore.YELLOW}Image:{Fore.RESET} ", Fore.YELLOW + thefeedentry['Links']['Image'] + Fore.RESET)
            else:
                print("--------------------------------------------------")
                print("Title: ", thefeedentry['Title'])
                print("Date: ", thefeedentry['Date'], end="\n\n")
                print("Alt image: ", thefeedentry['Alt image'])
                print(thefeedentry['Discription'], end="\n\n")
                print("Links: ")
                print("News: ", thefeedentry['Links']['News'])
                print("Image: ", thefeedentry['Links']['Image'])
