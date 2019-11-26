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
        dec_description: decorated description of article
        link: absolute URL to article
        pubDate: date of publication article
        media: all media objects from article
        source: absolute URL to containing RSS source
        links: all links from article without any formatting
        dec_links: decorated links from article in special format
    """
    title = peewee.TextField()
    description = peewee.TextField()
    dec_description = peewee.TextField()
    link = peewee.CharField(unique=True)
    pubDate = peewee.DateTimeField()
    media = peewee.TextField()
    source = peewee.ForeignKeyField(Source, backref='articles')
    links = peewee.TextField()
    dec_links = peewee.TextField()

    class Meta:
        database = DB_HANDLE
        db_table = "articles"
        order_by = ('-pubDate',)

    @classmethod
    def from_struct(cls, struct, source):
        """
        Class method for creating Article model object from given dict.
        Object creating with safe load a pub date. If RSS feed have no pub date,
        the article will be saved with the date of adding to the db.

        :param struct: dictionary with info about article
        :param source: Source object of source feeds. Used for connect sources with articles
        :type struct: dict
        :type source: Source
        :return: return Article object if no objects in db with such link. Else None
        :rtype: Article or None
        """
        try:
            if struct['pubDate'] != 'None':
                date = datetime.datetime.strptime(struct['pubDate'], "%a, %d %b %Y %H:%M")
            else:
                date = datetime.datetime.now()

            return cls.create(
                title=struct['title'],
                description=struct['description'],
                dec_description=struct['dec_description'],
                link=struct['link'],
                pubDate=date,
                media=json.dumps(struct['media']),
                source=source,
                links=json.dumps(struct['links']),
                dec_links=json.dumps(struct['dec_links'])
            )
        except peewee.IntegrityError:
            return None

    def to_dict(self):
        """
        Method for converting model objects to dict with all info.

        :return: dict with article info
        :rtype: dict
        """
        return {
            'title': self.title,
            'description': self.description,
            'dec_description': self.dec_description,
            'link': self.link,
            'pubDate': self.pubDate.strftime("%a, %d %b %Y %H:%M"),
            'media': json.loads(self.media),
            'source': self.source.url,
            'links': json.loads(self.links),
            'dec_links': json.loads(self.dec_links),
        }
