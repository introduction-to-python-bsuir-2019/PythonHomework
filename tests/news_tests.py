import unittest
from rss_reader.news import News


class NewsTest(unittest.TestCase):

    def setUp(self):
        self.useful_data = "DataClear"
        self.data_with_tags = "<strange tags>DataClear<really strange data>"

    def test_clear_from_tags(self):
        self.assertEqual(self.useful_data, News.clean_from_tags(self.data_with_tags))

    def test_parse_links(self):
        pass

    def test_parse_media(self):
        pass

    def test_create_fb2(self):
        pass

    def test_create_html(self):
        pass

    def test_to_json(self):
        pass


if __name__ == '__main__':
    unittest.main()
