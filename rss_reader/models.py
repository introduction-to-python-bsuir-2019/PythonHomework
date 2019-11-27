class Article:
    """Class for store article data in useful format"""

    def __init__(self, date, title, content, media, link):
        self.date = date
        self.title = title
        self.content = content
        self.media = media
        self.link = link

    def to_dict(self):
        """Convert article data at dict and return it"""
        return {'date': self.date.strftime("%d %m %Y"),
                'title': self.title,
                'content': self.content,
                'media': self.media,
                'link': self.link}

    def __repr__(self):
        return f'<Article: {self.date}, {self.title}>'
