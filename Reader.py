from NewsItem import NewsItem

import feedparser


class Reader:
    def __init__(self, rss_url):
        self._rss_url = rss_url
        self._news = list()

    def parse_rss(self):
        return feedparser.parse(self._rss_url)

    def get_news(self, amount_news):
        feed = self.parse_rss()
        for news_item in feed['items']:
            item = NewsItem(news_item.title, news_item['description'], news_item.link)
            self._news.append(item)
        return self._news[:amount_news]
