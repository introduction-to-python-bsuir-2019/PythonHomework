"""Module contains objects related to rss feed"""
import logging
import datetime
import time
from typing import Dict, List, Any

from bs4 import BeautifulSoup


class RSSFeed:
    """RSSFeed class"""
    def __init__(self, dict_args: Dict[str, Any], data: Dict[str, Any]):
        """Init RSSFeed class"""
        self.rss_url: str = dict_args['source']
        self.rss_feed: Dict[str, Any] = data
        self.news: List = []
        self.rss_feed_dict: Dict[str, Any] = {}

    def data_processing(self) -> Dict:
        """
        Method for converting rss data to a dictionary
        and correcting them,
        as well as processing the limit parameter
        """
        self.rss_feed_dict.update({
            "_id": int(time.time()),
            "Feed": self.rss_feed.feed.title,
            "Url": self.rss_url,
            "Date_Parsed": datetime.datetime.today().strftime("%Y%m%d")
        })
        logging.info('Update rss_feed_dict(Add Feed and Url)')

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
