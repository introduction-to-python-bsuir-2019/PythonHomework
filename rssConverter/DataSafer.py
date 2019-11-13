import shelve
from rssConverter.Exeptions import IncorrectDateOrURL


class NewsGetterSafer:

    @staticmethod
    def get_data(date, url):
        shelve_file = 'storage'
        key = date + url
        with shelve.open(shelve_file) as storage:
            if key in storage.keys():
                return storage[key]
            raise IncorrectDateOrURL(date, url)

    @staticmethod
    def save_data(url, news,  date):
        shelve_file = 'storage'
        with shelve.open(shelve_file) as storage:
            key = date+url
            storage[key] = news
