"""Module contains objects related to news"""
import logging
from typing import List, Dict
from datetime import date

from rssreader.base import BaseClass


class News(BaseClass):
    """News class"""
    def __init__(self, title: str, published: str, published_dt: date, link: str, description: str, hrefs: List[Dict]
                 ) -> None:
        self.title = title
        self.published = published  # a string in the same format as it was published in the original feed
        self.published_dt = published_dt
        self.link = link
        self.description = description
        self.hrefs = hrefs
        logging.info(f'Initialize news ({self.link})')

    def _get_hrefs_text(self) -> str:
        """Returns text representation of the links attribute"""
        logging.info(f'Convert links of news description ({self.link}) into string')
        return ''.join([f'[{i}]: {link["href"]} ({link["type"]})\n' for i, link in enumerate(self.hrefs)])

    def get_text(self) -> str:
        """Returns instance data in human-readable text format"""
        logging.info(f'Convert news ({self.link}) attributes into string')
        return f'Title: {self.title}\nDate: {self.published}\nLink: {self.link}\n\n{self.description}\n\n' \
               f'Links:\n{self._get_hrefs_text()}'

    def get_json_dict(self) -> Dict:
        """Returns required instance attributes as dictionary later to be used for json creating"""
        logging.info(f'Convert news ({self.link}) attributes into dictionary')
        return {'title': self.title, 'published': self.published, 'link': self.link, 'description': self.description,
                'hrefs': self.hrefs}
