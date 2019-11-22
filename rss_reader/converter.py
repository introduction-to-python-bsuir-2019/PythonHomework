from abc import ABC, abstractmethod


class ConverterBase(ABC):
    
    @abstractmethod
    def convert(self):
        return self
    
class PdfConverter(ConverterBase):
    pass

class EpubConverte(ConverterBase):
    pass

class MobiConverter(ConverterBase):
    pass

class Fb2Converter(ConverterBase):
    pass
    