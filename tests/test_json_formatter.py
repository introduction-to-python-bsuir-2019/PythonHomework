import unittest
from rss_reader.json_formatter import NewsJsonFormatter

class TestNewsReader(unittest.TestCase):
    def test_format(self):
        news = '{"Title": "hello"}'    
        self.assertEqual(NewsJsonFormatter.format(news), '{{"feed": {[{"Title": "hello"}]}}}')

if __name__ == '__main__':
    unittest.main()