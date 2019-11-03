from fpdf import FPDF

from PIL import Image
import requests
from io import BytesIO
import os

from rss_reader import NewsReader


def silent_remove(path):
    """
    Remove file which may not exists

    :param path: filepath
    :return: None
    """

    try:
        os.remove(path)
    except OSError:
        pass

class PdfNewsConverter(FPDF):
    """
    Easy-to-use pdf rss news converter

    """

    def __init__(self, items, asd):
        """

        :param items: Rss in dictionary
        """

        super(PdfNewsConverter, self).__init__()

        self.items = items

    def header(self):
        """
        Pdf file header

        :return: None
        """

        self.set_top_margin(-10)
        self.set_font('Times', 'I', 8)
        self.cell(100)
        self.ln(20)

        header = self.items['title']
        self.cell(w=0, h=10,
                  txt=header, align='C', ln=2)

    def footer(self):
        """
        Pdf file footer

        :return: None
        """

        self.set_y(-15)
        self.set_font('Times', 'I', 8)

        self.cell(0, 10,
                  'Page number ' + str(self.page_no()),
                  0, 0, 'C')

    def put_image(self, link):  # TODO: make image reading from buffer!
        """
        Downloads image from link and paste it in
        pdf file.
        If there is no image -> paste text 'No file'

        :param link: link to the image
        :return: None
        """

        filename = link.split('/')[-1] + '.jpg'

        try:
            response = requests.get(link)
            img = Image.open(BytesIO(response.content))
            img = img.convert('RGB')

            img.save(filename)
            img.close()

            self.set_x(self.w / 2 - 15)
            self.image(filename, type='jpg')
        except requests.exceptions.MissingSchema:

            self.cell(0, 10, 'No image', 0, 0, 'C')
        finally:
            self.set_x(0)
            silent_remove(filename)

    @staticmethod
    def change_encoding(txt):
        """
        Changes encoding to fpdf compatible

        :param txt: Text to encode
        :return: new-encoded text
        """

        return txt.encode('latin-1',
                          'replace').decode('latin-1')

    def add_news_page(self, item):
        """
        Writes info about one news

        :param item: one news dictionary
        :return: None
        """

        item = {key: self.change_encoding(value)
                for key, value in item.items()}

        title = item['title']
        pub_date = item['pubDate']
        link = item['link']
        description = item['description']
        image_link = item['imageLink']
        image_description = item['imageDescription']

        self.set_font('Times', 'I', 14)
        self.multi_cell(w=0, h=10,
                        txt=title, align='C')

        self.set_font('Times', 'I', 10)
        self.multi_cell(w=0, h=10,
                        txt=f'Date: {pub_date}', align='C')

        self.multi_cell(w=0, h=10,
                        txt=f'Link: {link}', align='C')

        self.set_font('Times', '', 12)
        self.multi_cell(w=0, h=5,
                        txt=description, align='L')

        self.put_image(image_link)

        self.set_font('Times', 'I', 10)
        self.multi_cell(w=0, h=5,
                        txt=f'Image description: {image_description}',
                        align='C')
        print(image_description)

        # self.cell(w=5, h=20, txt='', border=0, ln=20, align='L')

    def add_all_news(self):
        """
        Add all news information into pdf

        :return: None
        """

        self.add_page()

        for el, plot in self.items.items():
            if el != 'title':
                self.add_news_page(plot)


feed = NewsReader('https://news.yahoo.com/rss/', limit=None, cashing=False)
it = feed.items
it = it

pdf = PdfNewsConverter(it)

pdf.add_all_news()
pdf.output('news.pdf', 'F')
print(pdf.items)
