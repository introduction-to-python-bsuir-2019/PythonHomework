import unittest
import os
from rss_reader.converter import ConverterBase, PdfConverter, HtmlConverter


class TestNews(unittest.TestCase):
    def test_init_dir_for_images(self):
        self.assertEqual(ConverterBase.init_dir_for_images_from_news('tests'), 'tests')

    def test_check_image_link(self):
        self.assertEqual(ConverterBase.check_image_link('htttps://linkhttp:/nestedlink'), 'http:/nestedlink')

    def test_generate_filename_pdf(self):
        path_to_file = os.path.join(os.getcwd(),'tests/data_for_testing/')
        self.assertEqual(PdfConverter.generate_filename(path_to_file, 'news.pdf'), f'{path_to_file}1news.pdf')

    def test_generate_filename_html(self):
        path_to_file = os.path.join(os.getcwd(),'tests/data_for_testing/')
        self.assertEqual(PdfConverter.generate_filename(path_to_file, 'news.html'), f'{path_to_file}1news.html')


if __name__ == '__main__':
    unittest.main()
