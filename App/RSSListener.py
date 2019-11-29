import logging
from App.Portal import Portal
from App.Errors import FatalError
from App.Saver import Saver

class RSSListener:
    """Класс листенер. Обрабатывает новые rss ссылки.
    Постороен так, что в будущем при добавлении минимального функционала,
    будет обрабатывать и сохранять новости из разных источников"""

    def __init__(self, limit, json_flag):
        logging.info("Creating object RSSListener")
        self.limit = limit
        self.json_flag = json_flag
        self.portal = None

    def start(self, url):
        """Метод принимает url и пускает его в обработку"""
        logging.info("We begin to process the url")
        try:
            self.portal = Portal(url, self.limit)
            saver = Saver(self.portal.news)
            saver.start_saving()
        except FatalError:
            raise
        except Exception as e:
            raise FatalError("Something go wrong")
        try:
            self.portal.print(self.json_flag)
        except Exception as e:
            raise FatalError("Problems with printing")
