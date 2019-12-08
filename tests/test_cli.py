import unittest
from argparse import ArgumentParser
import rss_reader.cli as cli


class TestCli(unittest.TestCase):
    def test_directory(self):
        self.assertEqual(cli.validate_path('tests'), 'tests')

    def test_url(self):
        self.assertEqual(cli.validate_url('https://news.yahoo.com'), 'https://news.yahoo.com')
        with self.assertRaises(ValueError):
            cli.validate_url('http:/news.yahoo')

    def test_date(self):
        import datetime
        self.assertEqual(cli.validate_date('20191123'), datetime.date(2019, 11, 23))
        self.assertIsNone(cli.validate_date('20193212'))

    def test_make_config_dict(self):
        self.assertDictEqual(cli.mk_config_for_conversion('path', None), {'pdf': 'path'})
        self.assertDictEqual(cli.mk_config_for_conversion(None, 'path'), {'html': 'path'})
        self.assertDictEqual(cli.mk_config_for_conversion('path', 'path'), {'pdf': 'path', 'html': 'path'})

    def test_adding_arguments(self):
        self.assertIsInstance(cli.adding_arguments(), ArgumentParser)


if __name__ == '__main__':
    unittest.main()
