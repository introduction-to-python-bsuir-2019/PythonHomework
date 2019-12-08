"""This module contain class representing html utility converter """

from src.components.converter.html.html_converter import HtmlConverter
from pathlib import Path
from weasyprint import HTML, CSS


class PdfConverter(HtmlConverter):
    """
        This class implements HtmlConverter class and convert
        rss data into html format.

        Using weasyprint and jinja2 allows to using HtmlConverter
        methods instead of writing own logic for pdf converter

        Attributes:
            _log_Converter attribute contain log name converter

    """

    _log_Converter = 'PDF'

    def _save_render_file(self, output: str, encoding: str = 'UTF-8'):
        """
        This method overriding _save_render_file method and provide saving pdf data
        by weasyprint and jinja2 from html templating
        :param output: str
        :param encoding: ste
        :return: None
        """
        HTML(string=output, encoding=encoding).write_pdf(
            stylesheets=[CSS(string=self._template_processor.get_template('style.css.jinja2').render())], target=self._path
        )

        Path(self._path).chmod(0o755)
