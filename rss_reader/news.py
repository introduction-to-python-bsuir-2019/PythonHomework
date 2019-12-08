'''Module contain class related to news'''
from sqlalchemy import Column, String, DateTime, PickleType, Integer
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class News(Base):
    '''News class'''
    __tablename__ = 'news'
    id = Column(Integer, primary_key=True, autoincrement=True)
    feed = Column(String)
    title = Column(String)
    date = Column(DateTime)
    link = Column(String)
    description = Column(String)
    media_content = Column(PickleType)
    date_of_addition = Column(DateTime)

    def __init__(self, feed, title, date, link, description, media_content, date_of_addition):
        self.feed = feed
        self.title = title
        self.date = date
        self.link = link
        self.description = description
        self.media_content = media_content
        self.date_of_addition = date_of_addition

    def __str__(self, json=None):
        '''Method returns full text of the feed'''
        str_to_print = 'Feed: %s\nTitle: %s\nDate: %s\nLink: %s\n\n%s\n\nLinks:\n[1] %s --feed\n' % \
            (self.feed, self.title, self.date, self.link, self.description, self.link)
        if self.media_content[0]:
            for i in range(len(self.media_content)):
                str_to_print += '[%d] %s --image\n' % (i+2, self.media_content[i])
        return str_to_print

    def __call__(self):
        return self.feed, self.title, str(self.date), self.link, self.description, self.media_content
