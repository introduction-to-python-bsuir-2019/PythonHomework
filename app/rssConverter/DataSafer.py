import shelve
from app.rssConverter.Exeptions import IncorrectDateOrURL


class NewsGetterSafer:
    """Class for saving ang getting news to storage"""

    @staticmethod
    def get_data(date, url):
        """Retrieve  news from storage for specify url and date"""
        shelve_file = 'storage'
        key = date + url
        with shelve.open(shelve_file) as storage:
            if key in storage.keys():
                return storage[key]
            raise IncorrectDateOrURL(date, url)

    @staticmethod
    def save_data(url, news,  date):
        """Save news to storage for specify url and date"""
        shelve_file = 'storage'
        with shelve.open(shelve_file) as storage:
            key = date+url
            storage[key] = news
