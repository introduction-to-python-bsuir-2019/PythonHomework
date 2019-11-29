import logging
from App.Portal import Portal
from App.Errors import FatalError
from App.Saver import Saver

class RSSListener:
    """Класс листенер. Обрабатывает новые rss ссылки.
    Постороен так, что в будущем при добавлении минимального функционала,
    будет обрабатывать и сохранять новости из разных источников"""

    def __init__(self, limit, json_flag, date):
        logging.info("Creating object RSSListener")
        self.limit = limit
        self.json_flag = json_flag
        self.date = date
        self.portal = None

    def start(self, url):
        """Метод принимает url и пускает его в обработку"""
        logging.info("We begin to process the url")
        try:
            self.portal = Portal(url, self.limit)
            saver = Saver()
            saver.start_saving(self.portal.news)
            if self.date is not None:
                old_news = saver.load(self.date)
                if old_news is not None:
                    self.portal.load_new_news(old_news)
                    self.portal.print(self.json_flag)
                else:
                    print("Error: news haven't been founded")

            else:
                self.portal.print(self.json_flag)
        except FatalError:
            raise
        except Exception as e:
            raise FatalError("Something go wrong")
