import os

from django.http import FileResponse

from .converters import *


class ResponseBuilder:
    """
    Base class with base logic of converting and load file with result.
    """
    from_folder = '__cache__'
    extension = None
    converter = None

    def load(self, articles, filename):
        """
        Base method of loading file with result of executing program.

        :param articles: dict with articles for converting and output
        :param filename: name of file for output
        :type articles: dict
        :type filename: str
        :return:
        """
        result_response = self.load_result(articles, filename)
        result_response = os.path.join(self.from_folder, result_response)
        return FileResponse(open(result_response, 'rb'),
                            filename=result_response,
                            content_type='application/txt')

    def load_result(self, articles, filename):
        """
        Method of converting result. Return name of file with result.

        :param articles: dict with articles for converting and output
        :param filename: name of file for output
        :type articles: dict
        :type filename: str
        :return: name of file for output, if process if successful
        :rtype: str
        """
        return self.converter().print(articles, filename=self.this_filename(filename))

    def this_filename(self, filename):
        """
        Method for correct name of file for current format.

        :param filename:
        :return:
        """
        return filename + self.extension if not filename.endswith(self.extension) else filename


class PDFResponse(ResponseBuilder):
    """
    Class processing request articles to PDF format
    """
    extension = '.pdf'
    converter = PDFPrintResponseConverter


class JSONResponse(ResponseBuilder):
    """
    Class processing request articles to JSON format
    """
    extension = '.json'
    converter = JSONPrintResponseConverter


class HTMLResponse(ResponseBuilder):
    """
    Class processing request articles to HTML format
    """
    extension = '.html'
    converter = HTMLPrintResponseConverter


class SampleResponse(ResponseBuilder):
    """
    Class processing request articles without any format
    """
    extension = '.txt'
    converter = SamplePrintResponseConverter


class ResponseController:
    @staticmethod
    def load_result_into_file(articles, to_pdf=None, to_html=None, to_json=None, to_sample=None):
        if to_html is not None:
            return HTMLResponse().load(articles, filename=to_html)
        if to_pdf is not None:
            return PDFResponse().load(articles, filename=to_pdf)
        if to_json is not None:
            return JSONResponse().load(articles, filename=to_json)

        return SampleResponse().load(articles, filename=to_sample)
