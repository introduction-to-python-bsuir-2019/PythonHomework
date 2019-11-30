import unittest
import rss_reader.news as feed


class DateTest(unittest.TestCase):

    def setUp(self) -> None:
        self.useful_data = "DataClear"
        self.data_with_tags = "<strange tags>Data<really strange data>Clear"

    def test_clear_from_tags(self):
        self.assertEqual(self.useful_data, feed.clean_from_tags(self.data_with_tags))

    def _parse_links(self):
        pass

    def _parse_media(self):
        pass


if __name__ == '__main__':
    unittest.main()