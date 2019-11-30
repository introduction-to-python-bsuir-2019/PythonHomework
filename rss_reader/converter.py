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
                response, content = h.request(image)
                image = Image.open(io.BytesIO(content))
                #image.convert('RGB')
                image_file_name = path.join(self.dir_for_images, '%d%d.png'%(feed.id, number_of_image))
                image.save(image_file_name, 'PNG')
                #with open(image_file_name, 'wb') as out:
                 #   out.write(content)


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


class HTML2PDF(FPDF, HTMLMixin):
    pass


class PdfConverter(ConverterBase):
    def __init__(self, news, dir_for_save):
        super().__init__(news, dir_for_save)
        self.filename = 'news.pdf'
    
    def convert(self):
        pdf = HTML2PDF('P','mm', 'A4')
        pdf.add_font('TimesNewRoman', '', 'times-new-roman.ttf', uni=True)
        pdf.add_page()
        pdf.set_font('TimesNewRoman', size=22)
        pdf.set_left_margin(20)
        pdf.set_right_margin(15)
        pdf.cell(0, 20, 'News you were looking for', ln=1, align='C')
        for feed in self.news:
            pdf.set_font('TimesNewRoman', size=18)
            pdf.multi_cell(0, 10, feed.title, align='C')
            pdf.set_font('TimesNewRoman', 'U', 12)
            pdf.set_text_color(r=0, g=0, b=255)
            pdf.cell(210, 15, 'Link to that news', ln=1, align='L', link=feed.link)
            pdf.set_text_color(0,0,0)
            pdf.set_font('TimesNewRoman', size=14)
            pdf.write(6, feed.description)
            pdf.ln(10)
            for number_of_image in range(len(feed.media_content)):
                pdf.image(path.join(self.dir_for_images, '%d%d.png'%(feed.id, number_of_image)), 20, w=120, h=80)         
            
        #html_news = HtmlConverter(self.news, self.dir_for_images, False).convert()
        #pdf.write_html(html_news)
        pdf.output(self.filename)
        

class EpubConverte(ConverterBase):
    pass


class MobiConverter(ConverterBase):
    pass


class Fb2Converter(ConverterBase):
    pass

if __name__=='__main__':
    PdfConverter(123,'123').convert()