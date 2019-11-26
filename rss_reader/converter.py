from abc import ABC, abstractmethod


class ConverterBase(ABC):
    def __init__(self, news):
        self.news = news
        
    @abstractmethod
    def convert(self, news):
        return news
    

class HtmlConverter(ConverterBase): 

    def convert(self):
        return path


class PdfConverter(ConverterBase):
    
    def convert(self):
        return path


class EpubConverte(ConverterBase):
    pass


class MobiConverter(ConverterBase):
    pass


class Fb2Converter(ConverterBase):
    pass
    