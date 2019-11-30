import logging
from App.Portal import Portal
from App.Errors import FatalError
from App.Saver import Saver


class RSSListener:
    """"""

    def __init__(self, limit, json_flag, date, html_path, pdf_path):
        logging.info("Creating object RSSListener")
        self.limit = limit
        self.date = date
        self.portal = None
        self.json_flag = json_flag
        self.html_path = html_path
        self.pdf_path = pdf_path

    def start(self, url):
        """Class listener. Handles new rss links and saved news"""
        logging.info("We begin to process the url")
        try:
            self.portal = Portal(url, self.limit)
            saver = Saver()
            saver.start_saving(self.portal.news)
            if self.date is not None:
                old_news = saver.load(self.date)
                if old_news is not None:
                    self.portal.load_new_news(old_news)
                    self.printing()
                else:
                    print("Error: news haven't been founded")

            else:
                self.printing()
            if self.html_path is not None:
                self.portal.convert_to_html(self.html_path)
            if self.pdf_path is not None:
                self.portal.convert_to_pdf(self.pdf_path)
        except FatalError:
            raise
        except Exception as e:
            raise FatalError("Something go wrong")

    def printing(self):
        self.portal.print(self.json_flag)