from abc import ABC, abstractmethod


class ConverterBase(ABC):
    def __init__(self, news, dir_for_save):
        self.news = news
        
    @abstractmethod
    def convert(self, news):
        return news
    
    def save_file(self):
        pass
    
    def get_images(self, images):
        pass

class HtmlConverter(ConverterBase): 

    def convert(self):
        return path


class PdfConverter(ConverterBase):
    from fpdf import FPDF
    def convert(self):
        return path


class EpubConverte(ConverterBase):
    pass


class MobiConverter(ConverterBase):
    pass


class Fb2Converter(ConverterBase):
    pass
    