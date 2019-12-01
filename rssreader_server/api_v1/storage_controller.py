from .managers import ArticleManager, SourceManager


class StorageController:
    """
    Static controller for loading and saving articles in database.
    """

    @staticmethod
    def load(url, date, limit):
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
        articles = SourceManager.get_articles_with_data_from(clr_url, date)

        if limit is not None:
            articles['articles'] = [article for i, article in enumerate(articles['articles']) if i < limit]

        articles['articles'] = [article.to_dict() for article in articles['articles']]
        return articles

    @staticmethod
    def save(url, articles, title):
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
        source = SourceManager.get_or_create(clr_url, title)

        return ArticleManager.create_and_return(articles, source)
