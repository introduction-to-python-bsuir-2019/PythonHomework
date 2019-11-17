import logging
import feedparser
import json
from App.News import News


class Portal:
    """Класс служит для хранения и обработки информации свзянной с одним новостным порталом."""

    def __init__(self, url):
        logging.info("Creating object Portal")
        self.url = url
        rss = self.get_rss()
        try:
            self.title = rss.feed.title
            self.link = rss.feed.link
            self.updated = None
            self.news = []
            self.links = []
            self.update(rss.entries[::-1])
        except Exception as e:
            print("Problems with rss processing")
            logging.error(str(e))
            exit()

    def get_rss(self):
        """Получает rss файл"""
        logging.info("Getting rss file")
        try:
            return feedparser.parse(self.url)
        except Exception as e:
            print("Problems getting rss file")
            logging.error(str(e))
            exit()

    def update(self, entries):
        """Метод служит для получения(добавления новых в будущем) статей"""
        logging.info("Start processing article")
        try:
            rss = self.get_rss()
            if self.updated != rss.feed.updated:
                self.updated = rss.feed.updated
                for entry in entries:
                    self.news.insert(0, News(entry))
        except Exception as e:
            print("Problems with article processing")
            logging.error(str(e))
            exit()

    def print(self, limit, json_flag):
        """Метод выводит информацию о портале и о статьях"""
        if limit is None or limit > len(self.news):
            limit = len(self.news)
        if json_flag:
            logging.info("Saving to json")
            json_news = []
            for news in self.news[:limit]:
                json_news.append({"Title": news.title, "Date": news.date, "Link": news.link,
                                  "Summary": news.summary, "Images": news.images, "Links": news.links})
            main_dict = {"Title": self.title, "Url": self.url, "News": json_news}

            print(json.dumps(main_dict, ensure_ascii=False, indent=4))
        else:
            logging.info("Saving to text")
            print("\n\nRSS-chanel\n"
                  "Title: {0}\n".format(self.title))
            for news in self.news[:limit]:
                print("*" * 20 + "New article" + "*" * 20 + "\n{0}\n".format(news))
