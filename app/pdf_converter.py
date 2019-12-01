"""
    Contains class PDFConverter which receives path
    where it will save news in PDF format
"""

import os
import json
import warnings
from datetime import datetime

from bs4 import BeautifulSoup
import urllib.error
import urllib.request
import fpdf

from app.RSSReader import RSSReader


# To protect your fragile mind from BeautifulSoup warnings
warnings.filterwarnings("ignore")


class PDFConverter:
    """ Writes news in PDF file """

    def __init__(self, url, limit, date, to_pdf, logger, news=None):
        """ Sets up fonts for PDF file """

        self.url = url
        self.limit = limit
        self.date = date
        self.to_pdf = to_pdf
        self.news = news
        self.logger = logger

        fpdf.set_global('SYSTEM_TTFONTS', os.path.join(os.path.dirname(__file__), 'fonts'))
        self.pdf = fpdf.FPDF()
        self.pdf.add_font('NotoSans-Black', '', 'NotoSans-Black.ttf', uni=True)
        self.pdf.add_font('NotoSans-Thin', '', 'NotoSans-Thin.ttf', uni=True)

    def write_json_to_pdf(self):
        """ Writes cached JSON news into PDF file """

        self.write_title('Cached RSS news')

        file_path = 'cache' + os.path.sep + self.date + '.json'
        with open(file_path, encoding='utf-8') as rf:
            news = json.load(rf)

        for new in news:
            self.create_cells(new)
            self.pdf.ln(10)
            self.pdf.add_page()
        try:
            file_path = self.to_pdf + os.path.sep + 'cached_news.pdf'
            self.pdf.output(file_path)
        except FileNotFoundError:
            self.logger.info(f'Path to file {file_path} not found')
        else:
            self.logger.info('Cached news has been written to PDF file')

    def write_to_pdf(self):
        """ Writes news into PDF file """

        if not self.news:
            return

        self.write_title('RSS news')

        rss_reader = RSSReader(self.url, self.limit, self.date, self.logger)
        for new in self.news:
            new = rss_reader.to_dict(new)
            self.create_cells(new)
            self.pdf.ln(10)
            self.pdf.add_page()
        try:
            file_path = self.to_pdf + os.path.sep + 'news.pdf'
            self.pdf.output(file_path)
        except FileNotFoundError:
            self.logger.info(f'Path to file {file_path} not found')
        else:
            self.logger.info('News has been written to PDF file')

    def write_title(self, title):
        """ Writes title of PDF file """

        self.pdf.set_font('NotoSans-Black', size=16)
        self.pdf.add_page()
        self.pdf.set_title('News')
        self.pdf.cell(200, 10, txt=title, ln=1, align='C')
        self.pdf.cell(0, 10, ln=1)

    def create_cells(self, new):
        """ Creates cells in PDF file with news content """

        img_path = None
        for key, value in new.items():
            self.pdf.set_font('NotoSans-Black', size=12)
            self.pdf.cell(25, 5, txt=key + ': ', ln=0, align='L')
            self.pdf.set_font('NotoSans-Thin', size=12)
            if key == 'Image':
                self.pdf.multi_cell(0, 5, txt=BeautifulSoup(value, 'html.parser').text)
                img_path = self.download_image(value)
            else:
                self.pdf.multi_cell(0, 5, txt=value)
        if img_path:
            self.write_image(img_path)

    def download_image(self, img_url):
        """ Downloads image form given url and returns path """

        img = None
        directory_path = 'images' + os.path.sep
        if not os.path.exists(directory_path):
            self.logger.info('Creating directory images')
            os.mkdir(directory_path)

        img_name = self.create_image_name()
        try:
            img = urllib.request.urlopen(img_url).read()
        except ValueError:
            self.logger.info('Failed image download')
            return None
        except urllib.error.URLError:
            self.logger.info('The attempt to establish a connection was unsuccessful because '
                             'Due to incorrect response of already connected computer')

        try:
            img_path = os.path.abspath('') + os.path.sep + directory_path + img_name
            with open(img_path, "wb") as out:
                out.write(img)
        except FileNotFoundError:
            self.logger.info('Could not write image to folder images')
        else:
            self.logger.info('Image has been downloaded')
        return img_path

    def write_image(self, img_path):
        """ Writes image to pdf file """

        try:
            self.pdf.image(img_path)
        except SyntaxError:
            return None
        except RuntimeError:
            return None
        self.pdf.multi_cell(0, 10, txt=f'{img_path}')

    def create_image_name(self):
        """ Creates name for image using current time (YearMonthDay_HoursMinutesSeconds_Milliseconds.jpg) """

        img_name = datetime.today().strftime('%Y%m%d_%H%M%S_%f')
        img_name += '.jpg'
        return img_name
