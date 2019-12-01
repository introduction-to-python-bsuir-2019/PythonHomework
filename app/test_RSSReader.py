"""
    Tests for RSSReader class methods
"""

import unittest

from app.rss_reader import get_logger
from app.RSSReader import RSSReader
from app.rss_exception import RSSException


class TestRSSReader(unittest.TestCase):
    """ Some sort of genius tests """

    def setUp(self):
        url = 'https://www.google.com/'
        limit = 5
        date = '20191130'
        logger = get_logger()

        self.rss_reader = RSSReader(url, limit, date, logger)

    def test_get_feed(self):
        with self.assertRaises(RSSException):
            self.rss_reader.get_feed()

    def test_get_img_url(self):
        summary = '<p><a href="https://news.yahoo.com/ilhan-omar-gop-challenger-banned-173107211.html"><img ' \
                  'src="http://l1.yimg.com/uu/api/res/1.2/Q65f_fAoZ1bUNUPEZ9TzMQ--/YXBwaWQ9eXRhY2h5b247aD04Njt' \
                  '3PTEzMDs-/http://d.yimg.com/hd/cp-video-transcode/1009217/645bffba-5098-49ad-b36f-821308334' \
                  '5d7/ea5c7e80-890b-5ad5-9f04-e4005fb40434/data_3_0.jpg?s=343dee8421a4018296c99715b74b3886&c=c' \
                  '9bed65751ca54a241ff888a51cc4be0&a=tripleplay4us&mr=0" width="130" height="86" alt="Ilhan Oma' \
                  'r GOP challenger banned from Twitter after saying she should be &quot;tried for treason and ' \
                  'hanged”" align="left" title="Ilhan Omar GOP challenger banned from Twitter after saying she sh' \
                  'ould be &quot;tried for treason and hanged”" border="0" ></a>Danielle Stella campaign account ' \
                  'also tweeted a picture of a stick figure being hanged with a link to a blog post about her com' \
                  'ments.<p><br clear="all">'

        url = 'http://l1.yimg.com/uu/api/res/1.2/Q65f_fAoZ1bUNUPEZ9TzMQ--/YXBwaWQ9eXRhY2h5b247aD04Njt3PTEzMDs-/http:' \
              '//d.yimg.com/hd/cp-video-transcode/1009217/645bffba-5098-49ad-b36f-8213083345d7/ea5c7e80-890b-5ad5-' \
              '9f04-e4005fb40434/data_3_0.jpg?s=343dee8421a4018296c99715b74b3886&c=c9bed65751ca54a241ff888a51cc4be0&a' \
              '=tripleplay4us&mr=0'

        self.assertEqual(self.rss_reader.get_img_url(summary), url)


if __name__ == '__main__':
    unittest.main()
