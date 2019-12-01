import unittest
import os
from app.rssConverter.FB2Converter import FB2Converter
from app.rssConverter.New import New


class FB2ConverterTests(unittest.TestCase):
    """Class for testing fb2 converting"""

    def setUp(self):
        self.news = []
        self.testNew = New()
        self.news.append(self.testNew)
        self.image_dir = os.path.join(os.getcwd(), 'images')
        self.fb2_converter = FB2Converter(self.image_dir, self.news)

    def tearDown(self):
        if os.path.exists(os.path.join(os.getcwd(), "news.fb2")):
            os.remove(os.path.join(os.getcwd(), "news.fb2"))

    def test_image_dir_creating(self):
        """Test fb2 file creation"""
        current_dir = os.getcwd()
        self.image_path = os.path.join(current_dir, 'news.fb2')
        self.assertEqual(self.image_path, self.fb2_converter.create_fb2_file(current_dir))


if __name__ == '__main__':
    unittest.main()
