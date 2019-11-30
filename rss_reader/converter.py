import logging
from os import path, makedirs, mkdir
from abc import ABC, abstractmethod
from fpdf import FPDF, HTMLMixin, fpdf

class ConverterBase(ABC):
    def __init__(self, news, dir_for_save, saving_file=True):
        self.news = news
        self.saving_file = saving_file
        self.dir_for_images = path.join(dir_for_save, '.images_from_news') if saving_file else dir_for_save
        if saving_file:
            self.dir_for_save = dir_for_save
            self.init_dir_for_save()
            self.init_dir_for_images_from_news()
            self.get_images(news)
                    
    def init_dir_for_save(self):
        if path.exists(self.dir_for_save):
            logging.info('Directory %s already exists' % self.dir_for_save)          
        else:
            makedirs(self.dir_for_save)
            logging.info('Create directory %s for saving file' % self.dir_for_save)
            
    def init_dir_for_images_from_news(self):
        if path.exists(self.dir_for_images):
            logging.info('Directory %s already exists' % self.dir_for_images)
        else:
            mkdir(self.dir_for_images)
            logging.info('Create directory %s for saving images from news' % self.dir_for_images)
        
    @abstractmethod
    def convert(self, news):
        return news
    
    def save_file(self, data):
        with open(str(path.join(self.dir_for_save, self.filename)), 'w') as f:
            f.write(data)
    
    def get_images(self, news):
        import httplib2                     #this lib selected because it is much faster than urllib or requests(if you use caching of course)
        from PIL import Image
        import io
        h = httplib2.Http('.cache')
        for feed in news:
            images = feed.media_content
            for number_of_image, image in zip(range(len(images)), images):
                if not image:
                    continue                    
                image = self.check_image_link(image)
                response, content = h.request(image)
                image = Image.open(io.BytesIO(content))
                image_file_name = path.join(self.dir_for_images, '%d%d.png'%(feed.id, number_of_image))
                image.save(image_file_name, 'PNG')

    def check_image_link(self, image_link):
        where_sub_link = image_link.rfind('http')
        if where_sub_link:
            return image_link[where_sub_link:]


class HtmlConverter(ConverterBase): 
    def __init__(self, news, dir_for_save, saving_file=True):
        super().__init__(news, dir_for_save, saving_file)
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
                             <p><h3>{title}</h3></p>
<p><a href="{url}">Link to that feed</a></p>
<table width="100%" cellspacing="0" cellpadding="4">
<tr>
<td width="80%">
 <div class="word">{description}</div>
 </td>
 </tr>
 </table>
</p>
</p>
'''

        self.image_template = '<center><img alt src="{path}" ></center>'
        
    def convert(self):
        news_str = ''
        for feed in self.news:
            images_from_the_feed = ''
            for number_of_image in range(len(feed.media_content)):
                images_from_the_feed += self.image_template.format(path=path.join(self.dir_for_images, '%d%d.jpg'%(feed.id, number_of_image)))    
            news_str += self.feed_template.format(title=feed.title, url=feed.link, description=feed.description, img=images_from_the_feed)
        converted_data = self.html_template.format(news=news_str)
        return self.save_file(converted_data) if self.saving_file else converted_data        


class PdfConverter(ConverterBase):
    def __init__(self, news, dir_for_save):
        super().__init__(news, dir_for_save)
        self.filename = 'news.pdf'
    
    class PDF(FPDF):
        def __init__(self):
            super().__init__('P','mm', 'A4')
            self.add_font('TimesNewRoman', '', 'times-new-roman.ttf', uni=True)
            self.set_margins(30, 20, 10)
            self.set_auto_page_break(True, 20)
            self.add_page()
            self.set_font('TimesNewRoman', size=22)
            self.cell(0, 20, 'News you were looking for', ln=1, align='C')
            
        def footer(self):
            self.set_y(-20)
            self.set_font('TimesNewRoman', size=12)
            self.cell(0, 20, '%s' % self.page_no(), 0, 0, 'R')
            
        def add_link(self, link):
            self.set_font('TimesNewRoman', 'U', 12)
            self.set_text_color(r=0, g=0, b=255)
            self.cell(210, 15, 'Link to that news', ln=1, align='L', link=link)
            
            
        def add_title(self, title):
            self.set_font('TimesNewRoman', size=18)
            self.multi_cell(0, 10, title, align='C')
        
        def add_description(self, description):
            self.set_text_color(0,0,0)
            self.set_font('TimesNewRoman', size=14)        
            self.write(6, feed.description)
            self.ln(10)
        
        def add_images_from_the_feed(self, id, media_content):
            for number_of_image in range(len(media_content)):
                if not media_content[0]:
                    continue
                self.set_x(50)
                self.image(path.join(self.dir_for_images, '%d%d.png'%(id, number_of_image)), w=120, h=80)
                self.ln(10)
            
        def add_feed(self, feed):
            self.add_title(feed.title)
            self.add_link(feed.link)
            self.add_description(feed.description)            
            self.add_images_from_the_feed(feed.id, feed.media_content)
            self.ln(20)
                
    def convert(self):
        pdf = self.PDF()        
        for feed in self.news:
            pdf.add_feed(feed)
        pdf.output(path.join(self.dir_for_save, self.filename))
        

class EpubConverte(ConverterBase):
    pass


class MobiConverter(ConverterBase):
    pass


class Fb2Converter(ConverterBase):
    pass
