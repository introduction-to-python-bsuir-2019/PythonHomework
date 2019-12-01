import unittest
import os
from app.rssConverter.HtmlConverter import HtmlConverter
from app.rssConverter.New import New


class HtmlConverterTests(unittest.TestCase):
    """Class for testing html converting"""

    def setUp(self):
        self.news = []
        self.testNew = New()
        self.news.append(self.testNew)
        self.image_dir = os.path.join(os.getcwd(), 'images')
        self.html_converter = HtmlConverter(self.image_dir, self.news)

    def tearDown(self):
        if os.path.exists(os.path.join(os.getcwd(), "news.html")):
            os.remove(os.path.join(os.getcwd(), "news.html"))

    def test_image_dir_creating(self):
        """Test html file creation"""
        current_dir = os.getcwd()
        self.image_path = os.path.join(current_dir, 'news.html')
        self.assertEqual(self.image_path, self.html_converter.create_html_file(current_dir))


if __name__ == '__main__':
    unittest.main()
