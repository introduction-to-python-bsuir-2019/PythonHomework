import unittest
import rss_reader.news_date as news_date
from datetime import datetime


class DateTest(unittest.TestCase):

    def setUp(self) -> None:
        self.pattern = '%Y%m%d'
        self.date_tuple = (2019, 11, 28, 15, 22, 41, 3, 332, 0)
        self.pretty_date_str = 'Thu, 28 Nov 2019 15:22:41 +0000'

    def test_get_current_date_str(self):
        current_date = datetime.today()
        self.assertEqual(current_date.strftime(self.pattern), news_date.get_current_date_str())

    def test_get_current_date_tuple(self):
        self.assertEqual(datetime.now().utctimetuple(), news_date.get_current_date_tuple())

    def test_is_valid_date(self):
        self.assertTrue(news_date.is_valid_date('20191112'))
        self.assertFalse(news_date.is_valid_date('20193412'))

    def test_get_date_str(self):
        self.assertEqual(news_date.get_date_str(self.date_tuple), '20191128')

    def test_get_date_pretty_str(self):
        self.assertEqual(self.pretty_date_str, news_date.get_date_pretty_str(self.date_tuple))


if __name__ == '__main__':
    unittest.main()
