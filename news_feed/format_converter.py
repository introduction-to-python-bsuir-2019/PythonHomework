from fpdf import FPDF

from PIL import Image
import requests
from io import BytesIO
import os


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

    def __init__(self, items):
        """

        :param items: Rss in dictionary
        """

        super(PdfNewsConverter, self).__init__()

        self.items = items
        self.add_font('ArialNew',
                      fname=os.path.join('fonts', 'arial.ttf'),
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
            header = self.change_encoding(self.items['title'])
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
        except requests.exceptions.MissingSchema:
            self.set_x(0)
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

        return str(txt).encode('KOI8-R',
                               'replace').decode('KOI8-R')

        # return str(txt)

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
            else:
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

