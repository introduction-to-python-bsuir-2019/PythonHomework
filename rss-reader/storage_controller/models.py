"""
Module with description of models in database.
Used SQLite3 database and peewee module for work with it.

"""

import datetime

import peewee
import json

__all__ = ['DB_HANDLE', 'Source', 'Article']

STORAGE_DATABASE = 'storage.sqlite3'

DB_HANDLE = peewee.SqliteDatabase(STORAGE_DATABASE)


class Source(peewee.Model):
    """
    Model for containing rss feed sources in SQLite database.

    Fields:
        title: title of article
        url: absolute URL to RSS source
    """
    title = peewee.TextField(null=True)
    url = peewee.TextField(unique=True)

    class Meta:
        database = DB_HANDLE
        db_table = "sources"

    @classmethod
    def get_or_create(cls, url, title=None):
        """
        Rewriten base method of safe getting Source model object.

        :param url: string link for init object
        :param title: title of feeds source
        :type url: str
        :type title: str
        :return: Source object. If object with such data is founded return it,
            else created new object and return it.
        :rtype: Source
        """
        try:
            return super().get(Source.url == url)
        except peewee.DoesNotExist:
            return cls.create(url=url, title=title)

    def sort_by_date(self, date):
        """
        Method for get list of articles with a date after the given date.

        :param date: datetime for searching articles in string
        :type date: str
        :return: a list with of articles with a date after the given date
        :rtype: list
        """
        return self.articles.select().where(Article.pubDate >= date)


class Article(peewee.Model):
    """
    Model for containing rss feed article in SQLite database.
    All objects of this model ordered by pubDate field.

    Fields:
        title: title of article
        description: description of article
        link: absolute URL to article
        pubDate: date of publication article
        media: all media objects from article
        source: absolute URL to containing RSS source
        links: all links from article in specified format
    """
    title = peewee.TextField()
    description = peewee.TextField()
    link = peewee.CharField(unique=True)
    pubDate = peewee.DateField(formats=["%Y%m%d", ])
    media = peewee.TextField()
    source = peewee.ForeignKeyField(Source, backref='articles')
    links = peewee.TextField()

    class Meta:
        database = DB_HANDLE
        db_table = "articles"
        order_by = ('-pubDate',)

    @classmethod
    def from_dict(cls, struct, source):
        """
        Class method for creating Article model object from given dict.

        :param struct: dictionary with info about article
        :param source: Source object of source feeds. Used for connect sources with articles
        :type struct: dict
        :type source: Source
        :return: return Article object if no objects in db with such link. Else None
        :rtype: Article or None
        """
        try:
            return cls.create(
                title=struct['title'],
                description=struct['description'],
                link=struct['link'],
                pubDate=datetime.datetime.strptime(struct['pubDate'], "%a, %d %b %Y %H:%M:%S %z"),
                media=json.dumps(struct['media']),
                source=source,
                links=json.dumps(struct['links']),
            )
        except peewee.IntegrityError:
            return None

    def to_dict(self):
        return {
            'title': self.title,
            'description': self.description,
            'link': self.link,
            'pubDate': self.pubDate,
            'media': self.media,
            'source': self.source.url,
            'links': self.links,
        }
