from fpdf import FPDF

from PIL import Image
import requests
import base64
from io import BytesIO
import os

import news_feed


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


def change_encoding(txt):
    """
    Changes encoding to fpdf compatible

    :param txt: Text to encode
    :return: new-encoded text
    """

    return str(txt).encode('KOI8-R',
                           'replace').decode('KOI8-R')


class PdfNewsConverter(FPDF):
    """
    Easy-to-use pdf rss news converter

    """

    def __init__(self, items):
        """

        :param items: Rss in dictionary
        """

        super(PdfNewsConverter, self).__init__()

        path = os.path.join(os.path.dirname(news_feed.__file__), 'fonts', 'arial.ttf')

        self.items = items
        self.add_font('ArialNew',
                      fname=path,
                      uni='True')

    def header(self):
        """
        Pdf file header

        :return: None
        """

        self.set_top_margin(-10)
        self.set_font('ArialNew')
        # self.set_font('Arial', 'I', 8)
        self.cell(100)
        self.ln(20)

        try:
            header = change_encoding(self.items['title'])
        except KeyError:
            header = ''

        self.cell(w=0, h=10,
                  txt=header, align='C', ln=2)

    def footer(self):
        """
        Pdf file footer

        :return: None
        """

        self.set_y(-15)
        # self.set_font('Arial', 'I', 8)
        self.set_font('ArialNew')

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
        except (requests.exceptions.MissingSchema, OSError):
            self.set_x(0)
            self.cell(0, 10, 'No image', 0, 0, 'C')
        finally:
            self.set_x(0)
            silent_remove(filename)

    def add_news_page(self, item):
        """
        Writes info about one news

        :param item: one news dictionary
        :return: None
        """

        item = {key: change_encoding(value)
                for key, value in item.items()}

        title = item['title']
        pub_date = item['pubDate']
        link = item['link']
        description = item['description']
        image_link = item['imageLink']
        image_description = item['imageDescription']

        # self.set_font('Arial', 'I', 14)
        self.set_font('ArialNew')
        self.multi_cell(w=0, h=10,
                        txt=title, align='C')

        # self.set_font('Arial', 'I', 10)
        self.set_font('ArialNew')
        self.multi_cell(w=0, h=10,
                        txt=f'Date: {pub_date}', align='C')

        self.multi_cell(w=0, h=10,
                        txt=f'Link: {link}', align='C')

        # self.set_font('Arial', '', 12)
        self.set_font('ArialNew')
        self.multi_cell(w=0, h=5,
                        txt=description, align='L')

        self.put_image(image_link)

        # self.set_font('Arial', 'I', 10)
        self.set_font('ArialNew')
        self.multi_cell(w=0, h=5,
                        txt=f'Image description: {image_description}',
                        align='C')

        # self.cell(w=5, h=20, txt='', border=0, ln=20, align='L')

    def add_all_news(self):
        """
        Add all news information into pdf

        :return: None
        """

        self.add_page()

        for el, plot in self.items.items():
            if el != 'title' and el != 'title_image':
                self.add_news_page(plot)


class FB2NewsConverter:
    """
    Easy-to-use fb2 rss news converter

    """

    def __init__(self, items):
        self.items = items

    one_news_template = """
<body>
    <section id="{sectionId}">
        <title>
            <p>{title}</p>
        </title>
        <p><image l:href="#{imageLink}"/></p>  
        
        <p><emphasis>{pubDate}</emphasis></p>
                
        <p>{description}</p>
        <p><emphasis>{imageDescription}</emphasis></p>
        
        <p>Source:</p>
    </section>
</body>
<binary id="{imageLink}" content-type="image/jpeg">{image}</binary>
    """

    def add_one_news(self, item):
        """
        Add one news into one_news_template

        :param item: news in dict
        :return: filled template
        """

        item = {key: change_encoding(value)
                for key, value in item.items()}

        title = item['title']
        pub_date = item['pubDate']
        link = item['link']
        description = item['description']
        image_link = item['imageLink']
        image_description = item['imageDescription']
        binary_image = FB2NewsConverter.get_binary_image(image_link)

        template = self.one_news_template.format(
            sectionId=hash(title),
            title=title,
            pubDate=pub_date,
            # link=link,
            description=description,
            imageLink=str(hash(image_link)) + '.jpg',
            imageDescription=image_description,
            image=binary_image
        )

        return template

    @staticmethod
    def create_fb2_template():
        """
        Starting and ending of fb2 template

        :return: starting and ending of template
        """

        fb2_start = """<?xml version="1.0" encoding="windows-1251"?>
<FictionBook xmlns="http://www.gribuser.ru/xml/fictionbook/2.0" xmlns:l="http://www.w3.org/1999/xlink">
        """

        fb2_end = """
</FictionBook>
        """

        return fb2_start, fb2_end

    @staticmethod
    def create_fb2_description(title):
        """
        Fb2 description part

        :param title: title of rss source
        :return: description of fb2
        """

        fb2_description = f"""
            <description>
                <title-info>
                    <genre>home_entertain</genre>
                    <book-title>{title}</book-title>
                    <author>
                        <last-name>RSS</last-name>
                    </author>
                </title-info>
                <document-info>
                    <version>1.0</version>
                </document-info>
            </description>
        """

        return fb2_description

    @staticmethod
    def get_binary_image(image_link):
        """
        Returns description by link as base64 string

        :param image_link: link to image
        :return: image as base64 string
        """

        try:
            response = requests.get(image_link)
        except requests.exceptions.MissingSchema:
            return ''

        image = response.content
        image_bytes = base64.b64encode(image)

        return image_bytes.decode('UTF-8')

    def add_all_news(self):
        """
        Add all news into fb2 template

        :return: return resulting fb2 template
        """

        fb2_start, fb2_end = self.create_fb2_template()

        for key, plot in self.items.items():
            if key == 'title':
                fb2_start += self.create_fb2_description(plot)
            elif key != 'title_image':
                fb2_start += self.add_one_news(plot)

        res_fb2 = fb2_start + fb2_end

        return res_fb2

    def output(self, path):
        """
        Outputs resulting fb2 into file

        :param path: path into which we should add res fb2
        :return: None
        """

        res_fb2 = self.add_all_news()

        with open(path, 'w') as file:
            file.write(res_fb2)


class HTMLNewsConverter:
    """
    Easy-to-use html rss news-converter

    """

    def __init__(self, items):
        """

        :param items: Rss in dictionary
        """

        self.items = items

    one_news_template = """
            <h2>{title}</h2>
            <p>Date: {pubDate}</p>
            <a href='{link}'>News link</a>
            <p>{description}</p>
            <img src='{imageLink}', alt='No image'>
            <p>Image description: {imageDescription}</p>
    """

    def add_one_news(self, item):
        """
        Add one news info into html

        :param item: one news info
        :return: one news info into html
        """

        item = {key: change_encoding(value)
                for key, value in item.items()}

        title = item['title']
        pub_date = item['pubDate']
        link = item['link']
        description = item['description']
        image_link = item['imageLink']
        image_description = item['imageDescription']

        template = self.one_news_template.format(
            title=title,
            pubDate=pub_date,
            link=link,
            description=description,
            imageLink=image_link,
            imageDescription=image_description
        )

        return template

    @staticmethod
    def create_res_html_template():
        """
        Creates outer tags for whole html.

        :return: outer opening tags, outer closing tags
        """

        res_html_start = """
<!DOCTYPE html>
    <html>
        <body>
        """

        res_html_end = """
    </body>
</html>
        """

        return res_html_start, res_html_end

    @staticmethod
    def create_title(title):
        """
        Create tag for title of rss source

        :param title: title of rss source
        :return: title of rss source in html
        """

        title = f"""
            <h4>{title}</h4>
        """

        return title

    def add_all_news(self):
        """
        Add all news into html between outer
        opening tags and outer closing tags

        :return: resulting html file
        """

        res_html_start, res_html_end = self.create_res_html_template()

        for el, plot in self.items.items():
            if el == 'title':
                res_html_start += self.create_title(plot)
            elif el != 'title_image':
                res_html_start += self.add_one_news(plot)

        res_html = res_html_start + res_html_end

        return res_html

    def output(self, path):
        """
        Outputs resulting html into file

        :param path: path into which we should add res html
        :return: None
        """

        res_html = self.add_all_news()

        with open(path, 'w') as file:
            file.write(res_html)


#
# pdf = PdfNewsConverter(it)
#
# pdf.add_all_news()
# pdf.output('news.pdf', 'F')
#
# html = HTMLNewsConverter(it)
#
# html.output('news.html')

