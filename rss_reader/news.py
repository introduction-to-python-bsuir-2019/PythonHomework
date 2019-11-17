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

    def __init__(self, feed, title, date, description, link, media_content):
        self.feed = feed
        self.title = title
        self.date = date
        self.link = link
        self.description = description
        self.media_content = media_content

    def __repr__():
        pass
