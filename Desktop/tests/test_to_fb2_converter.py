"""Tests must be called from root project's directory."""
import unittest
import sys
import os
import xml.dom.minidom as minidom

sys.path.append(os.getcwd() + '/rssreader')

from rssreader.to_fb2_converter import FB2

TITLE = 'TITLE'
SUB_TITLE = 'SUB TITLE'

PIECE_OF_NEWS_TITLE = 'news title'
PIECE_OF_NEWS_DATE = '11.22.1963'
PIECE_OF_NEWS_LINK = 'link'
PIECE_OF_NEWS_CONTENT = 'Text here'

XML = f'<?xml version="1.0" ?>\n\
<FictionBook xmlns:l="http://www.w3.org/1999/xlink">\n\
\t<description/>\n\
\t<body>\n\
\t\t<title>\n\
\t\t\t<p>{TITLE}</p>\n\
\t\t</title>\n\
\t\t<p>{SUB_TITLE}</p>\n\
\t\t<section>\n\
\t\t\t<title>\n\
\t\t\t\t<p>{PIECE_OF_NEWS_TITLE}</p>\n\
\t\t\t</title>\n\
\t\t\t<p>{PIECE_OF_NEWS_DATE}</p>\n\
\t\t\t<p>{PIECE_OF_NEWS_LINK}</p>\n\
\t\t\t<empty-line/>\n\
\t\t\t<empty-line/>\n\
\t\t\t<p>{PIECE_OF_NEWS_CONTENT}</p>\n\
\t\t</section>\n\
\t</body>\n\
</FictionBook>'

TEMP_FILENAME = 'temp.fb2'


class TestFB2Converter(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass
        os.remove(TEMP_FILENAME)

    def test_write_to_file(self):
        fb2 = FB2()
        fb2.add_description_of_resource(title_info=TITLE, subtitle_info=SUB_TITLE, image_url='')
        fb2.add_section(title_info=PIECE_OF_NEWS_TITLE,
                        date=PIECE_OF_NEWS_DATE,
                        link=PIECE_OF_NEWS_LINK,
                        imgs_links=[],
                        content=PIECE_OF_NEWS_CONTENT)

        fb2.write_to_file(TEMP_FILENAME)

        result_xml = ''
        with open(TEMP_FILENAME) as file:
            result_xml = file.read()

        self.assertEqual(result_xml, XML)


if __name__ == '__main__':
    unittest.main()
