import unittest
from app.rssConverter.NewsPrinter import NewsPinter
from app.rssConverter.Exeptions import IncorrectLimit
from app.rssConverter.New import New


class RssNewsPrinterTests(unittest.TestCase):
    """Class for test NewsPrinter class"""

    def setUp(self):
        self.newsPrinter = NewsPinter()

    def test_get_limited_news(self):
        """Function  test getting limited news"""
        check_list = [1, 2]
        self.assertListEqual([1], self.newsPrinter.get_limited_news(check_list, 1))
        with self.assertRaises(IncorrectLimit):
            self.newsPrinter.get_limited_news(check_list, 10)

    def test_to_str_for_json(self):
        """Function  test getting json str"""
        check_str = '"1"'
        self.assertEqual(check_str, self.newsPrinter.to_str_for_json('1'))

    def test_in_json_format(self):
        check_str = '{ "news": [ { "title":"a" } ]}'
        self.testNew = New()
        self.testNew.items['title'] = "a"
        self.assertEqual(check_str, self.newsPrinter.in_json_format([self.testNew, ], 1))


if __name__ == '__main__':
    unittest.main()
