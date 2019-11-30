import logging
import feedparser
import json
from App.Errors import FatalError
from App.News import News
from App.ToHtml import ToHtml
from App.ToPDF import ToPDF
from termcolor import colored
from App.Colors import Colors


class Portal:
    """The class is used to store and process information associated with one news portal"""

    def __init__(self, url, limit):
        logging.info("Creating object Portal")
        self.url = url
        rss = self.get_rss()
        try:
            self.title = rss.feed.title
            self.link = rss.feed.link
            self.updated = None
            self.news = []
            self.limit = limit
            self.links = []
            self.update(rss.entries[::-1])
        except Exception as e:
            raise FatalError("Problems with rss processing")

    def get_rss(self):
        """Get rss file"""
        logging.info("Getting rss file")
        try:
            return feedparser.parse(self.url)
        except Exception as e:
            raise FatalError("Problems getting rss file")

    def update(self, entries):
        """The method is used to obtain articles"""
        logging.info("Start processing article")
        if self.limit is None or self.limit > len(entries):
            limit = len(entries)
        else:
            limit = self.limit
        try:
            rss = self.get_rss()
            if self.updated != rss.feed.updated:
                self.updated = rss.feed.updated
                for entry in entries[:limit]:
                    self.news.insert(0, News(entry, self.title))
        except FatalError:
            raise
        except Exception as e:
            raise FatalError("Problems with article processing")

    def load_new_news(self, news):
        if self.limit is None or self.limit > len(news):
            self.news = news
        else:
            self.news = news[:self.limit]

    def print(self, json_flag):
        """The method displays information about the portal and articles"""
        try:
            if json_flag:
                logging.info("Saving to json")
                json_news = []
                for news in self.news:
                    json_news.append({"Title": news.title, "Date": news.date, "Link": news.link,
                                      "Summary": news.summary, "Images": news.images, "Links": news.links})
                main_dict = {"Title": self.title, "Url": self.url, "News": json_news}

                print(json.dumps(main_dict, ensure_ascii=False, indent=4))
            else:
                logging.info("Saving to text")
                print(colored("\n\nRSS-chanel", Colors["other"]))
                for news in self.news:
                    print(colored("*" * 20 + "New article" + "*" * 20 + "\n", Colors["article"]))
                    print(colored(news, Colors["text"]))
        except Exception as e:
            logging.error(str(e))
            raise FatalError("Problems with printing")

    def convert_to_html(self, html_path):
        """Convert news to html"""
        logging.info("Start converting news to html")
        try:
            to_html = ToHtml(self.news, html_path)
            to_html.make_file()
        except Exception as e:
            print(colored("Error with converting to html", Colors["error"]))
            logging.info(str(e))

    def convert_to_pdf(self, pdf_path):
        """Convert news to pdf"""
        logging.info("Start converting news to pdf")
        try:
            to_html = ToHtml(self.news)
            to_pdf = ToPDF(to_html.html, pdf_path)
            to_pdf.make_file()
        except Exception as e:
            print(colored("Error with converting to pdf", Colors["error"]))
            logging.info(str(e))
