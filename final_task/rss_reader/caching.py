import os
import json
import rss_reader.news_date as news_date
import rss_reader.news as news


class Cache:

    def __init__(self, file_path):
        self.path = file_path
        self.content = {}

    def add_news(self, news_obj):
        """
        THis method adds news to cache
        :param news_obj: News class instance
        :return: None
        """
        if news_obj.source not in self.content:
            self.content[news_obj.source] = {}
        source_cache = self.content[news_obj.source]
        for item in news_obj.items:
            str_news_date = news_date.get_date_str(item.date)
            if str_news_date not in source_cache:
                date_news = news.News(news_obj.source)
                date_news.feed = news_obj.feed
                source_cache[str_news_date] = {'content': date_news.to_json(), 'links_list': []}
            links_list = source_cache[str_news_date]['links_list']
            if item.link not in links_list:
                links_list.append(item.link)
                source_cache[str_news_date]['content']['news']['items'].append(item.to_json())

    def get_news(self, source, date, count):
        """
        This function retrieves count news from cache by source an date
        :param source: str
        :param date: str
        :param count: int
        :return: News class instance or None
        """
        if source in self.content:
            if date in self.content[source]:
                news_from_cache = news.News.from_json(self.content[source][date].get('content'))
                if count > 0:
                    news_from_cache.items = news_from_cache.items[:count]
                return news_from_cache

    def load(self):
        """
        This method loads cache content from file into self.content
        :return: None
        """
        try:
            if not os.path.exists(self.path):
                with open(self.path, 'w') as cache_file:
                    cache_file.write("{}")
            else:
                with open(self.path, 'r') as cache_file:
                    self.content = json.load(cache_file)
        except Exception as e:
            raise e

    def dump(self):
        """
        This method writes cache content from self.content to file
        :return: None
        """
        try:
            with open(self.path, 'w') as cache_file:
                json.dump(self.content, cache_file, indent=2)
        except Exception as e:
            raise e
