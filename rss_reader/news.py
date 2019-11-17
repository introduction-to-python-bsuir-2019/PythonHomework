from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base


engine = create_engine('sqlite:///news.db')
Base = declarative_base()


class News(Base):
    __tablename__ = 'news'

    id = Column(Integer, primary_key=True, autoincrement=True)
    feed = Column(String)
    title = Column(String)
    date = Column(DateTime)
    link = Column(String)
    description = Column(String)
    media_content = Column(String)

    def __init__(self, feed, title, date, link, description, media_content):
        self.feed = feed
        self.title = title
        self.date = date
        self.link = link
        self.description = description
        self.media_content = media_content

    def __str__(self):
        return 'Feed: %s\nTitle: %s\nDate: %s\nLink: %s\n\n%s\n\nLinks:\n[1] %s (feed)\n[2] %s (image)\n' % \
            (self.feed, self.title, self.date, self.link, self.description, self.link, self.media_content)

    def __call__(self):
        return self.feed, self.title, self.date, self.link, self.description, self.media_content
