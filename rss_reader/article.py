"""Article module"""

import re
import time
import logging


class Article:
    def __init__(self, title, date, text, link, hrefs):
        self.title = title
        self.date = date
        self.text = self.strip_html_string(text)
        self.link = link.split('?')[0]
        self.hrefs = hrefs

    def convert_time_to_unix(self):
        """Convert datetime to unix time"""
        pattern_time = time.strptime(self.date, '%a, %d %b %Y %H:%M:%S %z')
        return int(time.mktime(pattern_time))

    def strip_html_string(self, string):
        """Remove html tags from a string"""
        strip_string = re.compile('<.*?>')
        return re.sub(strip_string, '', string)
