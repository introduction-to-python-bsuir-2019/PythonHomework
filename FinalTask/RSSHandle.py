import feedparser


class RssHandler:

    def __init__(self, rss: str):
        self.rss = rss
        self.feed = None
        self.feed_dict = {}

    def url_handler(self) -> object:
        """Takes URL and return rss object"""
        self.feed = feedparser.parse(self.rss)
        try:
            if self.feed.status % 100 != 2:
                raise Exception('Invalid URL!')
        except:
            raise Exception('Invalid URL!')
        return self.feed


    def rss_dict(self) -> dict:
        """Make dictionary from RSS-Feed"""
        self.feed_dict['source'] = self.feed['feed']['title']
        self.feed_dict['news'] = []
        for descr in self.feed['entries']:
            self.feed_dict['news'].append({'title':descr['title'],
            'pubDate':descr['published_parsed'],'text':descr['summary']})
        return self.feed_dict


    def to_json(self):
        """Make JSON file from RSS"""
        pass
