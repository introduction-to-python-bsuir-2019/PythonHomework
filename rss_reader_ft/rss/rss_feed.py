"""Module contains objects related to rss feed"""
import logging

from bs4 import BeautifulSoup


class RSSFeed:
    """RSSFeed class"""
    def __init__(self, dict_args, data):
        """Init RSSFeed class"""
        self.rss_url: str = dict_args['source']
        self.limit: int = dict_args['limit']
        self.rss_feed = data
        self.news = []
        self.rss_feed_dict = {}

    def data_processing(self) -> dict:
        """
        Method for converting rss data to a dictionary
        and correcting them,
        as well as processing the limit parameter
        """
        self.rss_feed_dict.update({
            "Feed": self.rss_feed.feed.title,
            "Url": self.rss_url
        })
        logging.info('Update rss_feed_dict(Add Feed and Url)')

        if self.limit is not None:
            self.rss_feed.entries = self.rss_feed.entries[:self.limit]
        logging.info('We take the amount of news equal to the limit')

        for entry in self.rss_feed.entries:
            soup = BeautifulSoup(entry.summary, features="html.parser")
            self.news.append({
                "Title": str(entry.title).replace("&#39;", "'"),
                "Date": entry.published,
                "Link": entry.link,
                "Description": soup.text,
                "Links": {
                    "Source_link": entry.links[0]["href"],
                    "Img_links": [link.get("src") for link in soup.find_all("img") if link.get("src")]
                }
            })
        logging.info('Append dict in News')

        self.rss_feed_dict.update({"News": self.news})
        logging.info('Update rss_feed_dict(Add News)')
        return self.rss_feed_dict
