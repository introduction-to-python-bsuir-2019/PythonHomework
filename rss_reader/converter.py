import logging
import os
from abc import ABC, abstractmethod


class ConverterBase(ABC):
    def __init__(self, news, dir_for_save):
        self.news = news
        self.dir_for_save = dir_for_save
        self.dir_for_images = os.path.join(dir_for_save, '.images_from_news')
        self.init_dir_for_save()
        self.init_dir_for_images_from_news()
        
    def init_dir_for_save(self):
        if os.path.exists(self.dir_for_save):
            logging.info('Directory %s already exists' % self.dir_for_save)
        else:
            os.mkdirs(self.dir_for_save)
            logging.info('Create directory %s for saving file' % self.dir_for_save)
            
    def init_dir_for_images_from_news(self):
        if os.path.exists(self.dir_for_save):
            logging.info('Directory %s already exists' % self.dir_for_images)
        else:
            os.mkdir(self.dir_for_images) 
            logging.info('Create directory %s for saving images from news' % self.dir_for_images)
        
    @abstractmethod
    def convert(self, news):
        return news
    
    def save_file(self, data):
        with open(str(os.path.join(self.dir_for_save, self.filename))) as f:
            f.write(self.data)
    
    def get_images(self, images):
        import httplib2                     #this lib selected because it is much faster than urllib or requests(if you use caching of course)
        h = httplib2.Http('.cache')
        for number, feed in zip(range(len(news)), news):
            response, content = h.request(feed)
            with open(os.path.join(self.dir_for_images, 'image%d.jpg' % number), 'wb') as image:
                image.write(content)
        

class HtmlConverter(ConverterBase): 
    def __init__(self, news, dir_for_save):
        super().__init__(news, dir_for_save)
        self.filename = 'news.html'

    def convert(self):
        return path


class PdfConverter(ConverterBase):
    from fpdf import FPDF
    def __init__(self, news, dir_for_save):
        super().__init__(news, dir_for_save)
        self.filename = 'news.pdf'
    
    def convert(self):
        return path


class EpubConverte(ConverterBase):
    pass


class MobiConverter(ConverterBase):
    pass


class Fb2Converter(ConverterBase):
    pass
