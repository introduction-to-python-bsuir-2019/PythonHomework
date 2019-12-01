import unittest
from unittest.mock import patch
import rss_reader


class TestReader(unittest.TestCase):

    def test_ultimately_unescape(self):
        self.assertEqual(rss_reader.ultimately_unescape('&quot;bread&quot; &amp; &quot;butter&quot;'),
                         '"bread" & "butter"')

    def test_hide(self):
        self.assertEqual(rss_reader.hide('u dont do dat to me do u d u do url', 'do', 'u'),
                         'u  d u rl')
        self.assertEqual(rss_reader.hide('u dont do dat to me do u do n', 'u', 'do'),
                         'nt do dat to me do  n')


if __name__ == '__main__':
    unittest.main()
