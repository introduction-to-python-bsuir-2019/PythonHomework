from src.components.converter.html.html_converter import HtmlConverter
from pathlib import Path
from weasyprint import HTML, CSS


class PdfConverter(HtmlConverter):

    _log_Converter = 'PDF'

    def _save_render_file(self, output, encoding: str='UTF-8'):
        HTML(string=output, encoding=encoding).write_pdf(
            stylesheets=[CSS(string=self._template_processor.get_template('style.css.jinja2').render())], target=self._path
        )

        Path(self._path).chmod(0o755)
