import unittest
from unittest.mock import MagicMock, patch

import datetime

from .rss_reader import NewsReader


class TestNewsReader(unittest.TestCase):
    def setUp(self) -> None:

        self.feed = NewsReader(url='no url')
        self.feed.items = {'title': 'CNN.com - RSS Channel - World',
                           0: {'title': "New Delhi is choking on smog and there's no end in sight",
                               'pubDate': 'Mon, 04 Nov 2019 09:59:11 GMT',
                               'link': 'http://rss.cnn.com/~r/rss/edition_world/~3/tbjRLXCRMIE/index.html',
                               'description': "• Air pollution reaches 'unbearable' levels",
                               'imageLink': 'http://feeds.feedburner.com/~r/rss/edition_world/~4/tbjRLXCRMIE',
                               'imageDescription': ''},
                           1: {'title': "World's most profitable company to IPO",
                               'pubDate': 'Mon, 04 Nov 2019 10:43:39 GMT',
                               'link': 'http://rss.cnn.com/~r/rss/edition_world/~3/WdGBNzqr0Ko/index.html',
                               'description': '',
                               'imageLink': 'http://feeds.feedburner.com/~r/rss/edition_world/~4/WdGBNzqr0Ko',
                               'imageDescription': ''},
                           2: {'title': 'China perfected fake meat centuries before the Impossible Burger',
                               'pubDate': 'Mon, 18 Oct 2019 09:19:17 GMT',
                               'link': 'http://rss.cnn.com/~r/rss/edition_world/~3/gb96p9WE7ow/index.html',
                               'description': '<a>If you\'re looking for a reason to care about tree loss,'
                                              ' the nation\'s latest heat wave <b>might</b> be it. Trees can lower'
                                              ' summer daytime temperatures by as much as 10 degrees'
                                              ' Fahrenheit, according to a recent study.</a>',
                               'imageLink': 'http://feeds.feedburner.com/~r/rss/edition_world/~4/gb96p9WE7ow',
                               'imageDescription': ''}}

    def test_get_date(self):
        date_0 = str(self.feed.get_date(self.feed.items[0]['pubDate']))
        res_date_0 = '19-11-2999'
        self.assertNotEqual(date_0, res_date_0)

        date_1 = str(self.feed.get_date(self.feed.items[1]['pubDate']))
        res_date_1 = '2019-11-04'
        self.assertEqual(date_1, res_date_1)

        date_2 = str(self.feed.get_date(self.feed.items[2]['pubDate']))
        res_date_2 = '2019-10-18'
        self.assertEqual(date_2, res_date_2)

    def test_get_description(self):
        description_0 = self.feed.get_description(self.feed.items[0]['description'])
        res_description_0 = '• Air pollution reaches \'unbearable\' levels'
        self.assertEqual(description_0, res_description_0)

        description_1 = self.feed.get_description(self.feed.items[1]['description'])
        res_description_1 = ''
        self.assertEqual(description_1, res_description_1)

        description_2 = self.feed.get_description(self.feed.items[2]['description'])
        res_description_2 = 'If you\'re looking for a reason to care about tree loss, ' \
                            'the nation\'s latest heat wave might be it. Trees can ' \
                            'lower summer daytime temperatures by as much as 10 degrees ' \
                            'Fahrenheit, according to a recent study.'
        self.assertEqual(description_2, res_description_2)

    def test_get_image(self):
        image_tag_0 = '<img src="https://developer.ibm.com/recipes/wp-content/uploads/sites/41/2018/02/Python.png" ' \
                      'alt="Some image">'
        image_src_0, image_alt_0 = self.feed.get_image(image_tag_0)

        res_image_src_0 = 'https://developer.ibm.com/recipes/wp-content/uploads/sites/41/2018/02/Python.png'
        res_image_alt_0 = 'Some image'

        self.assertEqual(image_src_0, res_image_src_0)
        self.assertEqual(image_alt_0, res_image_alt_0)

        image_tag_1 = '<img src="" ' \
                      'alt="">'
        image_src_1, image_alt_1 = self.feed.get_image(image_tag_1)

        res_image_src_1 = ''
        res_image_alt_1 = ''

        self.assertEqual(image_src_1, res_image_src_1)
        self.assertEqual(image_alt_1, res_image_alt_1)

    @patch('requests.get')
    def test_get_news(self, requests_get):
        with open('req.txt', encoding='UTF-8') as file:
            requests_get.return_value.text = file.readline()

        news = self.feed.get_news()
        res_news = {'title': 'Yahoo News - Latest News & Headlines',
                    'title_image': 'http://l.yimg.com/rz/d/yahoo_news_en-US_s_f_p_168x21_news.png',
                    0: {'title': 'After Trump&#39;s intervention, Navy SEAL Eddie Gallagher returns to work, for now',
                        'pubDate': 'Mon, 25 Nov 2019 18:38:58 -0500',
                        'link': 'https://news.yahoo.com/after-trumps-intervention-navy-'
                                'seal-eddie-gallagher-returns-to-work-for-now-233858319.html',
                        'description': 'Eddie Gallagher, the Navy SEAL at the center of a '
                                       'controversy in a case that President Trump intervened'
                                       ' in, went to work Monday, unsure of what lay ahead.',
                        'imageLink': 'http://l2.yimg.com/uu/api/res/1.2/'
                                     'YHHUCq3gwGzw04YakK775Q--/YXBwaWQ9eX'
                                     'RhY2h5b247aD04Njt3PTEzMDs-/https://'
                                     'media-mbst-pub-ue1.s3.amazonaws.com/'
                                     'creatr-images/2019-11/aa8c02a0-0c79-11ea-b1fd-1011ee5d77f0',
                        'imageDescription': "After Trump's intervention, Navy "
                                            "SEAL Eddie Gallagher returns to work, for now"}}

        self.assertEqual(news, res_news)


if __name__ == '__main__':
    unittest.main()
