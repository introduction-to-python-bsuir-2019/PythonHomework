import logging
from App.Portal import Portal
from App.Errors import FatalError

class RSSListener:
    """Класс листенер. Обрабатывает новые rss ссылки.
    Постороен так, что в будущем при добавлении минимального функционала,
    будет обрабатывать и сохранять новости из разных источников"""

    def __init__(self, limit, json_flag):
        logging.info("Creating object RSSListener")
        self.portals = []
        self.limit = limit
        self.json_flag = json_flag

    def start(self, url):
        """Метод принимает url и пускает его в обработку"""
        logging.info("We begin to process the url")
        try:
            self.portals.append(Portal(url))
        except FatalError:
            raise
        except Exception as e:
            raise FatalError("Something go wrong")
        try:
            self.portals[0].print(self.limit, self.json_flag)
        except Exception as e:
            raise FatalError("Problems with printing")
