import html
import time
from unittest import TestCase, main

from rssreader.html_parser import A, Img, HTMLParser

__all__ = ['TestA', 'TestImg', 'TestHTMLParser']


def equals_classes_a(obj1: A, obj2: A):
    return obj1.href == obj2.href


def equals_classes_img(obj1: Img, obj2: Img):
    return obj1.src == obj2.src and \
           obj1.alt == obj2.alt and \
           obj1.width == obj2.width and \
           obj1.height == obj2.height


class TestImg(TestCase):
    def setUp(self):
        self.fields = {
            'src': 'some_src',
            'alt': 'some_alt',
            'style': 'some_style',
            'width': 'some_width',
            'height': 'some_height',
        }
        self.img = Img(**self.fields)

    def test_create_obj(self):
        self.assertTrue(issubclass(type(self.img), Img))

        self.assertFalse(self.img is Img)

    def test_creating_fields(self):
        self.assertEqual(self.img.src, self.fields['src'])

        self.assertEqual(self.img.alt, self.fields['alt'])

        self.assertEqual(self.img.width, self.fields['width'])

        self.assertEqual(self.img.height, self.fields['height'])

    def test_method_link(self):
        self.assertEqual(self.img.link(), self.img.src)

        self.assertEqual(self.img.link(), self.fields['src'])

        self.assertNotEqual(self.img.link(), 'src')

    def test_method_format_link(self):
        ind = 1
        self.assertEqual(self.img.format_link(ind), f"[{ind}]: {self.img.src} (image)")

        self.assertEqual(self.img.format_link(2), "[2]: some_src (image)")

        self.assertNotEqual(self.img.format_link(3), "[1]: some_src (image)")

    def test_method_str(self):
        self.assertEqual(str(self.img), "[Image {}: %s] " % self.img.alt)

        self.assertNotEqual(str(self.img), "[Image {}: {}]")


class TestA(TestCase):
    def setUp(self):
        self.fields = {
            'href': 'some_href',
            'style': 'some_style',
            'align': 'some_align',
        }
        self.a = A(**self.fields)

    def test_create_obj(self):
        self.assertTrue(issubclass(type(self.a), A))

        self.assertFalse(self.a is A)

    def test_creating_fields(self):
        self.assertEqual(self.a.href, self.fields['href'])

        self.assertNotEqual(self.a.href, 'href')

        self.assertEqual(self.a.style, self.fields['style'])

    def test_method_link(self):
        self.assertEqual(self.a.link(), self.a.href)

        self.assertEqual(self.a.link(), self.fields['href'])

        self.assertNotEqual(self.a.link(), 'href')

    def test_method_format_link(self):
        ind = 1
        self.assertEqual(self.a.format_link(ind), f"[{ind}]: {self.a.href} (link)")

        self.assertEqual(self.a.format_link(2), "[2]: some_href (link)")

        self.assertNotEqual(self.a.format_link(3), "[1]: some_href (link)")

    def test_method_str(self):
        self.assertEqual(str(self.a), "[link {}]")

        self.assertNotEqual(str(self.a), "[link ]")


class TestHTMLParser(TestCase):
    def setUp(self):
        date = time.struct_time((2019, 11, 26, 20, 53, 11, 1, 330, 0))
        self.response = {
            'feed': {
                'title': 'Yahoo News - Latest News & Headlines',
            },
            'entries': [{
                'title': 'Some title',
                'description': '<p><a href="some long link"><img src="some long link to source of image 2" width="130" height="86" alt="Alt of image 2"></a>Some long description<p><br clear="all">',
                'link': 'some long link',
                'published_parsed': date,
            }]
        }
        self.article = {
            'title': 'Some title',
            'description': '<p><a href="some long link"><img src="some long link to source of image 2" width="130" height="86" alt="Alt of image 2"></a>Some long description<p><br clear="all">',
            'link': 'some long link',
            'published_parsed': date,
        }
        self.article_parsed = {
            'title': 'Some title',
            'description': 'Some long description',
            'dec_description': '[link 1][Image 2: Alt of image 2] Some long description',
            'link': 'some long link',
            'pubDate': 'Tue, 26 Nov 2019 20:53',
            'media': [{
                'src': 'some long link to source of image 2',
                'alt': 'Alt of image 2',
                'width': '130',
                'height': '86'
            }],
            'links': [
                'some long link',
                'some long link to source of image 2'
            ],
            'dec_links': [
                '[1]: some long link (link)',
                '[2]: some long link to source of image 2 (image)'
            ]
        }
        self.response_parsed = {
            'title': 'Yahoo News - Latest News & Headlines',
            'articles': [{
                'title': 'Some title',
                'description': 'Some long description',
                'dec_description': '[link 1][Image 2: Alt of image 2] Some long description',
                'link': 'some long link',
                'pubDate': 'Tue, 26 Nov 2019 20:53',
                'media': [{
                    'src': 'some long link to source of image 2',
                    'alt': 'Alt of image 2',
                    'width': '130',
                    'height': '86'
                }],
                'links': [
                    'some long link',
                    'some long link to source of image 2'
                ],
                'dec_links': [
                    '[1]: some long link (link)',
                    '[2]: some long link to source of image 2 (image)'
                ]
            }]
        }

        self.parser = HTMLParser()

    def test_parse(self):
        self.assertEqual(self.parser.parse(self.response, 1), self.response_parsed)

    def test_clear_from_html(self):
        string = 'some_string'
        self.assertEqual(self.parser._clear_from_html(html.escape(string)), string)

        dict_with_html_string = {
            1: html.escape('st&ri`ng'),
            'a': html.escape('s"tr>>i@ng\''),
            html.escape('s"tr>>i@ng\''): html.escape('s"tr>>i@ng\'')
        }
        result = {
            1: 'st&ri`ng',
            'a': 's"tr>>i@ng\'',
            's"tr>>i@ng\'': 's"tr>>i@ng\''
        }
        self.assertEqual(self.parser._clear_from_html(dict_with_html_string), result)

        list_with_html_string = [
            1,
            html.escape('st&ri`ng'),
            'a',
            html.escape('s"tr>>i@ng\'')
        ]
        result = [
            1,
            'st&ri`ng',
            'a',
            's"tr>>i@ng\'',
        ]
        self.assertEqual(self.parser._clear_from_html(list_with_html_string), result)

    def test_get_limited_articles(self):
        self.assertEqual(self.parser._get_limited_articles(self.response, 1), [self.article])

    def test_get_next_tag(self):
        line_with_tags = '<a href="some_href">'
        self.assertEqual(self.parser._get_next_tag(line_with_tags), (0, len(line_with_tags)))

        line_with_tags = '<img src="some_src" alt="some_alt">'
        self.assertEqual(self.parser._get_next_tag(line_with_tags), (0, len(line_with_tags)))

        line_with_tags = '<a href="some_href"'
        self.assertEqual(self.parser._get_next_tag(line_with_tags), None)

    def test_create_tag(self):
        params = {
            'a': True,
            'href': 'some_href',
        }
        self.assertTrue(equals_classes_a(self.parser._create_tag(params), A(**params)))

        params = {
            'img': True,
            'src': 'some_src',
            'alt': 'some_alt',
            'width': 'some_width',
            'height': 'some_height',
        }
        self.assertTrue(equals_classes_img(self.parser._create_tag(params), Img(**params)))

        params = {
            '<img': True,
            'src': 'some_src',
        }
        self.assertEqual(self.parser._create_tag(params), None)

    def test_get_params_from_line(self):
        full_tag = '<a href="some_href">'
        self.assertEqual(self.parser._get_params_from_line(full_tag), {'a': True,
                                                                       'href': 'some_href'})

        full_tag = '<img src="some_src" width="some_width" height="some_height" alt="some_alt">'
        self.assertEqual(self.parser._get_params_from_line(full_tag), {'img': True,
                                                                       'src': 'some_src',
                                                                       'width': 'some_width',
                                                                       'height': 'some_height',
                                                                       'alt': 'some_alt'})

    def test_get_all_strings(self):
        string = 'br clear="all"'
        self.assertEqual(self.parser._get_all_strings(string), (['all'], 'br clear='))

        string = 'a href="some_href"'
        self.assertEqual(self.parser._get_all_strings(string), (['some_href'], 'a href='))

        string = 'img src="some_src" width="some_width" height="some_height" alt="some_alt"'
        self.assertEqual(self.parser._get_all_strings(string), (['some_src', 'some_width', 'some_height', 'some_alt'],
                                                                'img src= width= height= alt='))

    def test_process_description(self):
        self.assertEqual(
            self.parser._process_description(self.article['description'], fill_desc=True, fill_links=True),
            (
                self.article_parsed['dec_description'],
                self.article_parsed['dec_links']
            )
        )

        self.assertEqual(
            self.parser._process_description(self.article['description'], fill_desc=False, fill_links=True),
            (
                self.article_parsed['description'],
                self.article_parsed['dec_links']
            )
        )

        self.assertEqual(
            self.parser._process_description(self.article['description'], fill_desc=True, fill_links=False),
            (
                self.article_parsed['dec_description'],
                self.article_parsed['links']
            )
        )

        self.assertEqual(
            self.parser._process_description(self.article['description'], fill_desc=False, fill_links=False),
            (
                self.article_parsed['description'],
                self.article_parsed['links']
            )
        )

    def test_article_to_dict(self):
        self.assertEqual(self.parser._article_to_dict(self.article), self.article_parsed)


if __name__ == '__main__':
    main()
