"""
    Contains class Converter which receives path
    where it will save news in PDF format
"""

import fpdf
import os
import json
from app.RSSreader import RSSreader


class Converter:
    """ Writes news in PDF file """

    def __init__(self, args, logger, news=None):
        self.arguments = args
        self.args = args.get_args()
        self.news = news
        self.logger = logger

        # fpdf.set_global('SYSTEM_TTFONTS', os.path.join(os.path.dirname(__file__), 'fonts'))
        fpdf.set_global('SYSTEM_TTFONTS', os.path.abspath('fonts'))
        self.pdf = fpdf.FPDF()
        self.pdf.add_font('NotoSans-Black', '', 'NotoSans-Black.ttf', uni=True)
        self.pdf.add_font('NotoSans-Thin', '', 'NotoSans-Thin.ttf', uni=True)

    def write_json_to_pdf(self):
        """ Writes cached JSON news into PDF file """

        self.write_title('Cached RSS news')

        file_path = 'cache' + os.path.sep + self.args.date + '.json'
        with open(file_path, encoding='utf-8') as rf:
            news = json.load(rf)

        for new in news:
            self.create_cells(new)
            self.pdf.ln(10)

        file_path = self.args.to_pdf + os.path.sep + 'cached_news.pdf'
        self.pdf.output(file_path)
        self.logger.info('Cached news has been written to PDF file')

    def write_to_pdf(self):
        """ Writes news into PDF file """

        if not self.news:
            return

        self.write_title('RSS news')

        rss_reader = RSSreader(self.arguments, self.logger)
        for new in self.news:
            new = rss_reader.to_json(new)
            self.create_cells(new)
            self.pdf.ln(10)

        file_path = self.args.to_pdf + os.path.sep + 'news.pdf'
        self.pdf.output(file_path)
        self.logger.info('News has been written to PDF file')

    def write_title(self, title):
        """Writes title of PDF file"""

        self.pdf.set_font('NotoSans-Black', size=16)
        self.pdf.add_page()
        self.pdf.set_title('News')
        self.pdf.cell(200, 10, txt=title, ln=1, align='C')
        self.pdf.cell(0, 10, ln=1)

    def create_cells(self, new):
        """ Creates cells in PDF file with news content """

        for key, value in new.items():
            self.pdf.set_font('NotoSans-Black', size=12)
            self.pdf.cell(25, 5, txt=key + ': ', ln=0, align='L')
            self.pdf.set_font('NotoSans-Thin', size=12)
            self.pdf.multi_cell(0, 5, txt=value)
