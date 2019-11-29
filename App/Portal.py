import logging
import feedparser
import json
from App.Errors import FatalError
from App.News import News


class Portal:
    """Класс служит для хранения и обработки информации свзянной с одним новостным порталом."""

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
        """Получает rss файл"""
        logging.info("Getting rss file")
        try:
            return feedparser.parse(self.url)
        except Exception as e:
            raise FatalError("Problems getting rss file")

    def update(self, entries):
        """Метод служит для получения(добавления новых в будущем) статей"""
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
        """Метод выводит информацию о портале и о статьях"""
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
                print("\n\nRSS-chanel")
                for news in self.news:
                    print("*" * 20 + "New article" + "*" * 20 + "\n{0}\n".format(news))
        except Exception as e:
            logging.error(str(e))
            raise FatalError("Problems with printing")
