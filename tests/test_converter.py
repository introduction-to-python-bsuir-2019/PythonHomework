import unittest
from rss_reader.converter import ConverterBase, PdfConverter, HtmlConverter


class TestNews(unittest.TestCase):
    def test_init_dir_for_images(self):
        self.assertEqual(ConverterBase.init_dir_for_images_from_news('tests'), 'tests')

    def test_check_image_link(self):
        self.assertEqual(ConverterBase.check_image_link('htttps://linkhttp:/nestedlink'), 'http:/nestedlink')


if __name__ == '__main__':
    unittest.main()
