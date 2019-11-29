import logging
from os import path, makedirs, mkdir
from abc import ABC, abstractmethod


class ConverterBase(ABC):
    def __init__(self, news, dir_for_save):
        self.news = news
        self.dir_for_save = dir_for_save
        self.dir_for_images = path.join(dir_for_save, '.images_from_news')
        self.init_dir_for_save()
        self.init_dir_for_images_from_news()
        
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
    
    def get_images(self):
        import httplib2                     #this lib selected because it is much faster than urllib or requests(if you use caching of course)
        h = httplib2.Http('.cache')
        for feed in self.news:
            images = feed.media_content
            for number_of_image, image in zip(range(len(images)), images):
                response, content = h.request(image)
                image_file_name = path.join(self.dir_for_images, '%s%d.jpg'%(feed.title, number_of_image))
                with open(image_file_name, 'wb') as out:
                    out.write(content)


class HtmlConverter(ConverterBase): 
    def __init__(self, news, dir_for_save):
        super().__init__(news, dir_for_save)
        self.filename = 'news.html'
        self.html_template = '''
<html>
    <head>
        <meta charset="utf-8">
        <title>News you were looking for</title>
    </head>
    <body>
        <center><h1>News you were looking for</h1></center>
        {news}
    </body>
</html>'''


        self.feed_template = '''
                             <h3><center><p>{title}</p></center></h3>
<p><a href="{url}">Link to that feed</a></p>
<table>
<tr>{description}</tr><br>
<tr><center>{img}</center></tr>
</table>
'''

        self.image_template = '<img src="{path}" ><br>'
        
    def convert(self):
        self.get_images()
        news_str = ''
        for feed in self.news:
            images_from_the_feed = ''
            for number_of_image in range(len(feed.media_content)):
                images_from_the_feed += self.image_template.format(path=path.join(path.basename(self.dir_for_images), '%s%d.jpg'%(feed.title, number_of_image)))              
            news_str += self.feed_template.format(title=feed.title, url=feed.link, description=feed.description, img=images_from_the_feed)
        self.save_file(self.html_template.format(news=news_str))  


class PdfConverter(ConverterBase):
    from fpdf import FPDF
    def __init__(self, news, dir_for_save):
        super().__init__(news, dir_for_save)
        self.filename = 'news.pdf'
    
    def convert(self):
        pass


class EpubConverte(ConverterBase):
    pass


class MobiConverter(ConverterBase):
    pass


class Fb2Converter(ConverterBase):
    pass
