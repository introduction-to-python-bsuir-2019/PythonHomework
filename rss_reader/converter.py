'''Module contains classes that implement converters in different formats'''
import logging
import httplib2
import io
from PIL import Image
from os import path, mkdir
from abc import ABC, abstractmethod
from fpdf import FPDF


class ConverterBase(ABC):
    '''Base class of converters'''
    def __init__(self, news, dir_for_save):
        self.news = news
        self.dir_for_save = dir_for_save
        self.dir_for_images = self.init_dir_for_images_from_news(path.join(dir_for_save, '.images_from_news'))
        self.get_images(news)

    @staticmethod
    def init_dir_for_images_from_news(dir_for_images):
        '''Method creates directory where images from the news wiil be saved'''
        if path.exists(dir_for_images):
            logging.info('Directory %s already exists' % dir_for_images)
        else:
            mkdir(dir_for_images)
            logging.info('Create directory %s for saving images from news' % dir_for_images)
        return dir_for_images

    @abstractmethod
    def convert(self, news):
        return news

    def save_file(self, data):
        '''Method that save converted file'''
        logging.info('Saving file with news')
        with open(self.generate_filename(self.dir_for_save, self.filename), 'w') as f:
            f.write(data)

    @staticmethod
    def generate_filename(dir_for_save, filename):
        '''Method that generate unique filename in the directory'''
        new_filename = path.join(dir_for_save, filename)
        number_of_files = 1
        while number_of_files:
            if path.exists(new_filename):
                new_filename = path.join(dir_for_save, str(number_of_files) + filename)
                number_of_files += 1
            else:
                return new_filename

    def get_images(self, news):
        '''Method that getting images that were in the news from their sources'''
        h = httplib2.Http('.cache')
        logging.info('Getting images from news')
        for feed in news:
            images = feed.media_content
            for number_of_image, image in enumerate(images):
                if not image:
                    continue
                image = self.check_image_link(image)
                response, content = h.request(image)
                image = Image.open(io.BytesIO(content))
                image_file_name = path.join(self.dir_for_images, f'{feed.id}{number_of_image}.png')
                image.save(image_file_name, 'PNG')

    @staticmethod
    def check_image_link(image_link):
        '''
        Method checks nested links in the source of image.
        
        For example, in news.yahoo.com link to the image has nested link 
        that contains the address of this image in its original form.
        '''
        logging.info('Checking for nested links')
        where_sub_link = image_link.rfind('http')
        if where_sub_link:
            return image_link[where_sub_link:]


class HtmlConverter(ConverterBase):
    '''Class implements conversion into HTML format'''
    def __init__(self, news, dir_for_save):
        logging.info('Initialization of HtmlConverter')
        super().__init__(news, dir_for_save)
        self.filename = 'news.html'
        self.html_template = '''
<html>
    <head>
        <meta charset="utf-8">
    </head>
    <body>
        <center><h1>News you were looking for</h1></center>
        <p>{news}</p>
    </body>
</html>'''

        self.feed_template = '''
                             <p>
                             <p><center><h3>{title}</h3></center></p>
<p><a href="{url}">Link to that feed</a></p>
<table width="100%" cellspacing="0" cellpadding="4">
<tr>
<td width="80%">
 <div class="word">{description}</div>
 </td>
 </tr>
 </table>
 <p>
 {img}
 </p>
</p>
</p>
'''

        self.image_template = '<center><img src="{path}" width="720" height="468"></center>'

    def convert(self):
        '''Method that doing conversion'''
        logging.info('Converting news to HTML format')
        news_str = ''
        for feed in self.news:
            images_from_the_feed = ''
            for number_of_image in range(len(feed.media_content)):
                images_from_the_feed += self.image_template.format(path=path.join(self.dir_for_images, f'{feed.id}{number_of_image}.png'))
            news_str += self.feed_template.format(title=feed.title, url=feed.link, description=feed.description, img=images_from_the_feed)
        converted_data = self.html_template.format(news=news_str)
        self.save_file(converted_data)


class PdfConverter(ConverterBase):
    '''Class that implements conversion into PDF format'''
    def __init__(self, news, dir_for_save):
        logging.info('Initialization of PdfConverter')
        super().__init__(news, dir_for_save)
        self.filename = 'news.pdf'

    class PDF(FPDF):
        '''Class implements PDF document'''
        def __init__(self, dir_with_images):
            logging.info('Initialization of PDF document')
            self.dir_with_images = dir_with_images
            super().__init__(orientation='P', unit='mm', format='A4')
            self.add_font('TimesNewRoman', fname='times-new-roman.ttf', uni=True)
            self.set_margins(left=30, top=20, right=10)
            self.set_auto_page_break(True, margin=20)
            self.add_page()
            self.set_font('TimesNewRoman', size=22)
            self.cell(0, 20, 'News you were looking for', ln=1, align='C')

        def footer(self):
            '''Method that adds footer to document'''
            self.set_y(-20)
            self.set_font('TimesNewRoman', size=12)
            self.cell(0, 20, '%s' % self.page_no(), 0, 0, 'R')

        def add_feed(self, feed):
            '''Method that adds feed to document'''
            self.add_title(feed.title)
            self.add_link(feed.link)
            self.add_description(feed.description)
            self.add_images_from_the_feed(feed.id, feed.media_content)
            self.ln(20)
            
        def add_link(self, link):
            '''Method that adds link to document'''
            self.set_font('TimesNewRoman', 'U', 12)
            self.set_text_color(r=0, g=0, b=255)
            self.cell(210, 15, 'Link to that news', ln=1, align='L', link=link)

        def add_title(self, title):
            '''Method that adds title of the feed to document'''
            self.set_font('TimesNewRoman', size=18)
            self.multi_cell(0, 10, title, align='C')

        def add_description(self, description):
            '''Method that adds description of the feed to document'''
            self.set_text_color(0, 0, 0)
            self.set_font('TimesNewRoman', size=14)
            self.write(6, description)
            self.ln(10)

        def add_images_from_the_feed(self, id, media_content):
            '''Method that adds images from the news to document'''
            for number_of_image in range(len(media_content)):
                if not media_content[0]:
                    continue
                self.set_x(50)
                self.image(path.join(self.dir_with_images, f'{id}{number_of_image}.png'), w=120, h=80)
                self.ln(10)

    def convert(self):
        '''Method that doing conversion'''
        logging.info('Converting news to PDF format')
        pdf = self.PDF(self.dir_for_images)
        for feed in self.news:
            pdf.add_feed(feed)
        logging.info('Saving news in PDF format')
        pdf.output(self.generate_filename(self.dir_for_save, self.filename))


class EpubConverte(ConverterBase):
    pass


class MobiConverter(ConverterBase):
    pass


class Fb2Converter(ConverterBase):
    pass
