from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class News(Base):
    __tablename__ = 'news'
    
    id = Column(Integer, primary_key=True, increment=1)
    title = Column(String(100))
    description = Column(Text)
    date = Column(Date)
    link = Column(Text)
    media_content = Column(Text)
    
    def __repr__():
        pass
    
    
    