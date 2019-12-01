import unittest
from app.rssConverter.RssConverter import RssConverter
from app.rssConverter.New import New


class RssConverterTests(unittest.TestCase):
    """Class for test RssConverter class"""

    def setUp(self):
        self.rssConverter = RssConverter()

    def test_parse_news(self):
        """Test for rssConverter.parse_news"""
        self.notParsedNew = [dict(title='Plane crash kills nine, injures three in South Dakota',
                                  title_detail={'type': 'text/plain', 'language': None,
                                                'base': 'https://news.yahoo.com/rss',
                                                'value': 'Plane crash kills nine, injures three in South Dakota'},
                                  summary='<p><a href="https://news.yahoo.com/plane-crash-kills-nine-injures-three'
                                          '-south-dakota-042236507.html"><img '
                                          'src="http://l2.yimg.com/uu/api/res/1.2/tzvj7g0Ju.jNcLAk3jqrBg'
                                          '--/YXBwaWQ9eXRhY2h5b247aD04Njt3PTEzMDs-/http://media.zenfs.com/en_us/News'
                                          '/afp.com '
                                          '/246321db0ddb94f202489f1fd666d10597689261.jpg" width="130" height="86" '
                                          'alt="Plane '
                                          'crash kills nine, injures three in South Dakota" align="left" title="Plane '
                                          'crash '
                                          'kills nine, injures three in South Dakota" border="0" ></a>A plane crash '
                                          'in the US '
                                          'state of South Dakota killed nine people, including two children, '
                                          'and injured three '
                                          'others on Saturday while a winter storm warning was in place, officials '
                                          'said.  The '
                                          'Pilatus PC-12, a single-engine turboprop plane, crashed shortly after '
                                          'take-off '
                                          'approximately a mile from the Chamberlain airport, the Federal Aviation '
                                          'Administration (FAA) said.  Among the dead was the plane\'s pilot, '
                                          'Brule County '
                                          'state\'s attorney Theresa Maule Rossow said, adding that a total of 12 '
                                          'people had '
                                          'been on board.<p><br clear="all">',
                                  summary_detail={'type': 'text/html', 'language': None,
                                                  'base': 'https://news.yahoo.com/rss',
                                                  'value': '<p><a href="https://news.yahoo.com/plane-crash-kills-nine'
                                                           '-injures '
                                                           '-three-south-dakota-042236507.html"><img '
                                                           'src="http://l2.yimg.com/uu/api/res/1.2/tzvj7g0Ju'
                                                           '.jNcLAk3jqrBg '
                                                           '--/YXBwaWQ9eXRhY2h5b247aD04Njt3PTEzMDs-/http://media'
                                                           '.zenfs.com '
                                                           '/en_us/News/afp.com'
                                                           '/246321db0ddb94f202489f1fd666d10597689261.jpg" '
                                                           'width="130" height="86" alt="Plane crash kills nine, '
                                                           'injures three '
                                                           'in South Dakota" align="left" title="Plane crash kills '
                                                           'nine, '
                                                           'injures three in South Dakota" border="0" ></a>A plane '
                                                           'crash in the '
                                                           'US state of South Dakota killed nine people, including two '
                                                           'children, and injured three others on Saturday while a '
                                                           'winter storm '
                                                           'warning was in place, officials said.  The Pilatus PC-12, '
                                                           'a single-engine turboprop plane, crashed shortly after '
                                                           'take-off '
                                                           'approximately a mile from the Chamberlain airport, '
                                                           'the Federal '
                                                           'Aviation Administration (FAA) said.  Among the dead was '
                                                           'the '
                                                           'plane\'s pilot, Brule County state\'s attorney Theresa '
                                                           'Maule Rossow '
                                                           'said, adding that a total of 12 people had been on '
                                                           'board.<p><br '
                                                           'clear="all">'},
                                  links=[{'rel': 'alternate', 'type': 'text/html',
                                          'href': 'https://news.yahoo.com/plane-crash-kills-nine-injures-three-south'
                                                  '-dakota '
                                                  '-042236507.html'}],
                                  link='https://news.yahoo.com/plane-crash-kills-nine-injures-three-south-dakota'
                                       '-042236507.html',
                                  published='Sat, 30 Nov 2019 23:22:36 -0500',
                                  source={'href': 'http://www.afp.com/', 'title': 'AFP'},
                                  id='plane-crash-kills-nine-injures-three-south-dakota-042236507.html',
                                  guidislink=False,
                                  media_content=[{'height': '86',
                                                  'url': 'http://l2.yimg.com/uu/api/res/1.2/tzvj7g0Ju.jNcLAk3jqrBg'
                                                         '--/YXBwaWQ9eXRhY2h5b247aD04Njt3PTEzMDs-/http://media.zenfs'
                                                         '.com/en_us '
                                                         '/News/afp.com/246321db0ddb94f202489f1fd666d10597689261.jpg',
                                                  'width': '130'}], media_text={'type': 'html'},
                                  media_credit=[{'role': 'publishing company'}], credit=''), ]

        self.testNew = New()
        self.testNew.items['title'] = "Plane crash kills nine, injures three in South Dakota"
        self.testNew.items['summary'] = 'A plane crash in the US ' \
                                        'state of South Dakota killed nine people, including two children, ' \
                                        'and injured three ' \
                                        'others on Saturday while a winter storm warning was in place, officials ' \
                                        'said.  The ' \
                                        'Pilatus PC-12, a single-engine turboprop plane, crashed shortly after ' \
                                        'take-off ' \
                                        'approximately a mile from the Chamberlain airport, the Federal Aviation ' \
                                        'Administration (FAA) said.  Among the dead was the plane\'s pilot, ' \
                                        'Brule County ' \
                                        'state\'s attorney Theresa Maule Rossow said, adding that a total of 12 ' \
                                        'people had ' \
                                        'been on board.'
        self.testNew.items['link'] = 'https://news.yahoo.com/plane-crash-kills-nine-injures-three-south-dakota' \
                                     '-042236507.html '
        self.testNew.items['published'] = 'Sat, 30 Nov 2019 23:22:36 -0500'
        self.testNew.items['images'] = 'http://l2.yimg.com/uu/api/res/1.2/tzvj7g0Ju.jNcLAk3jqrBg' \
                                       '--/YXBwaWQ9eXRhY2h5b247aD04Njt3PTEzMDs-/http://media.zenfs.com/en_us/News/afp' \
                                       '.com /246321db0ddb94f202489f1fd666d10597689261.jpg'
        self.testNew.items['links'] = ['https://news.yahoo.com/plane-crash-kills-nine-injures-three-south-dakota'
                                       '-042236507.html', ]
        self.result = self.rssConverter.parse_news(self.notParsedNew)[0]
        self.assertEqual(self.testNew.items['title'], self.result.items["title"])
        self.assertEqual(self.testNew.items['summary'], self.result.items['summary'])
        self.assertEqual(self.testNew.items['published'], self.result.items['published'])
        self.assertEqual(self.testNew.items['images'], self.result.items['images'])
        self.assertListEqual(self.testNew.items['links'], self.result.items['links'])


if __name__ == '__main__':
    unittest.main()
