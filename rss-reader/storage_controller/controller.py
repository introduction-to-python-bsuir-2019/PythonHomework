"""
Module with controllers for work with db.

"""
import json
import logging
import datetime

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

        logging.info(f"Completed. Converting date each article")
        articles['articles'] = [self._convert_date(article) for article in articles['articles']]

        logging.info(f"Completed. Load from JSON links each article")
        articles['articles'] = [self._load_links(article) for article in articles['articles']]

        logging.info(f"Completed. Load from JSON media each article")
        articles['articles'] = [self._load_media(article) for article in articles['articles']]

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

    @staticmethod
    def _load_media(article):
        """
        Method for converting media of a given article from JSON.

        :param article: article with media in JSON
        :type article: Article
        :return: article with correct media
        :rtype: Article
        """
        article.media = json.loads(article.media)
        return article

    @staticmethod
    def _load_links(article):
        """
        Method for converting links of a given article from JSON.

        :param article: article with links in JSON
        :type article: Article
        :return: article with correct links
        :rtype: Article
        """
        article.links = json.loads(article.links)
        return article

    @staticmethod
    def _convert_date(article, from_fmt="%Y-%m-%d", to_fmt="%a, %d %b %Y"):
        """
        Method for converting date of a given article to specific format.

        :param article: article with incorrect format of date
        :param from_fmt: optional parameter. Format to convert from
        :param to_fmt: optional parameter. Format to convert to
        :type article: Article
        :type from_fmt: str
        :type to_fmt: str
        :return: Article object with correct format of date
        :rtype: Article
        """
        _date = datetime.datetime.strptime(article.pubDate, from_fmt)
        article.pubDate = datetime.datetime.strftime(_date, to_fmt)
        return article
