"""
    Contains class PDFConverter which receives path
    where it will save news in PDF format
"""

import os
import json
import warnings

from bs4 import BeautifulSoup
import urllib.request
import fpdf

from app.RSSReader import RSSReader


warnings.filterwarnings("ignore")


class PDFConverter:
    """ Writes news in PDF file """

    def __init__(self, args, logger, news=None):
        """ Sets up fonts for PDF file """

        self.arguments = args
        self.args = args.get_args()
        self.news = news
        self.logger = logger

        fpdf.set_global('SYSTEM_TTFONTS', os.path.join(os.path.dirname(__file__), 'fonts'))
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
            self.pdf.add_page()

        file_path = self.args.to_pdf + os.path.sep + 'cached_news.pdf'
        self.pdf.output(file_path)
        self.logger.info('Cached news has been written to PDF file')

    def write_to_pdf(self):
        """ Writes news into PDF file """

        if not self.news:
            return

        self.write_title('RSS news')

        rss_reader = RSSReader(self.arguments, self.logger)
        for new in self.news:
            new = rss_reader.to_dict(new)
            self.create_cells(new)
            self.pdf.ln(10)
            self.pdf.add_page()

        file_path = self.args.to_pdf + os.path.sep + 'news.pdf'
        self.pdf.output(file_path)
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
        img_name = self.create_image_name(img_url)
        try:
            img = urllib.request.urlopen(img_url).read()
        except ValueError:
            self.logger.info('Failed download')
            return None
        img_path = os.path.abspath('') + os.path.sep + directory_path + img_name
        with open(img_path, "wb") as out:
            out.write(img)
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

    def create_image_name(self, img_url):
        """
            Image URL looks like
            'https://media-mbst-pub-ue1.s3.amazonaws.com/creatr-images/2019-11/aa8c02a0-0c79-11ea-b1fd-1011ee5d77f0'
            (without '.jpg' at the end)
            or
            'https://img.tyt.by/thumbnails/n/minsk/0a/10/proektnoe_predlozhenie_ulyanovskaya_belorusskaya.jpg'
            (with '.jpg' at the end)
            This method gets last part of url after '/' and adds '.jpg' if it is missing
            So image name will look like 'aa8c02a0-0c79-11ea-b1fd-1011ee5d77f0.jpg'
        """

        split_list = img_url.split('/')
        img_name = split_list[-1]
        if '.jpg' in img_name:
            return img_name
        img_name += '.jpg'
        return img_name
