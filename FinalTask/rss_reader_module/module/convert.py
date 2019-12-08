import jinja2
import os
import logging
from datetime import datetime
import base64

class ConvertTo:

    def __init__(self, feed, path):

        self.feed = feed
        self.env = None
        self.dir = os.path.join(os.path.dirname(__file__), 'templates')
        self.path = path

        self.create_env()

    def create_env(self):
        """Creates environment for jinja2."""

        logging.info("Creating environment for jinja2 templates.")
        self.env = jinja2.Environment(loader = jinja2.FileSystemLoader(self.dir))

    def to_html(self):
        "Convert dictionary in HTML format."

        html_template = self.env.get_template('html/templ.html')
        filepath = os.path.join(os.getcwd(), self.path, self.feed['Name'] + '.html')
        logging.info('Creating HTML file.')
        with open(filepath, 'w+') as html_file:
            html_file.write(html_template.render(feed=self.feed))

    def to_fb2(self):
        "Convert dictionary in XML format."

        fb2_template = self.env.get_template('xml/templ.xml')
        filepath = os.path.join(os.getcwd(), self.path, self.feed['Name'] + '.fb2')
        logging.info('Creating fb2 file.')
        with open(filepath, 'w+') as fb2_file:
            fb2_file.write(fb2_template.render(feed=self.feed, date=datetime.now()))
