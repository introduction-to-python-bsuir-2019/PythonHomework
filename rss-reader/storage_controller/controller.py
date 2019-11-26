"""
Module with controllers for work with db.

"""
import logging
from peewee import PeeweeException

from storage_controller.managers import *

__all__ = ['StorageController']


class StorageController:
    """
    Controller for loading and saving articles in database.
    """

    def __init__(self):
        try:
            DB_HANDLE.connect()
            self.articles = ArticleManager()
            self.sources = SourceManager()
        except PeeweeException as e:
            print(e)
            return

    def load(self, url, date, limit):
        """
        Method for loading limited articles from database

        :param url: source URL for getting articles from db
        :param date: date from which need to load articles in string
        :param limit: limit of articles for loading
        :type url: str
        :type date: str
        :type limit: int
        :return: list of dicts of articles with date after a given date
        :rtype: list
        """

        clr_url = url.strip('/\\')
        logging.info(f"Start loading articles from storage")
        articles = self.sources.get_articles_with_data_from(clr_url, date)

        logging.info(f"Completed. Cutting list of articles")
        if limit is not None:
            articles['articles'] = [article for i, article in enumerate(articles['articles']) if i < limit]

        logging.info(f"Completed. Convert to dict each article")
        articles['articles'] = [article.to_dict() for article in articles['articles']]

        return articles

    def save(self, url, articles, title):
        """
        Method for saving parsed articles.

        :param url: string URL of RSS source
        :param articles: parsed articles
        :param title: title of RSS source
        :type url: str
        :type articles: list
        :type title: str
        :return: count of new created articles in db
        :rtype: int
        """
        clr_url = url.strip('/\\')

        logging.info(f"Getting source model")
        source = self.sources.get_or_create(clr_url, title)

        logging.info(f"Completed. Saving articles in chosen source model")
        count = self.articles.create_and_return(articles, source)
        return count
