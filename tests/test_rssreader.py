import unittest
import glob
from rss_reader.rssreader import RSSReader
from datetime import datetime


class TestNews(unittest.TestCase):

    maxDiff = None

    def test_parse_html(self):
        rss_example = RSSReader('source', 1, datetime(2019, 12, 1), True, {}, False)
        html_example = '''<p><a href="https://news.yahoo.com/ilhan-omar-gop-challenger-banned-173107211.html"><img src="http://l1.yimg.com/\
uu/api/res/1.2/Q65f_fAoZ1bUNUPEZ9TzMQ--/YXBwaWQ9eXRhY2h5b247aD04Njt3PTEzMDs-\
/http://d.yimg.com/hd/cp-video-transcode/1009217/645bffba-5098-49ad-b36f-8213083345d7/ea5c7e80-890b-5ad5-\
9f04-e4005fb40434/data_3_0.jpg?s=343dee8421a4018296c99715b74b3886&c=c9bed65751ca54a241ff888a51cc4be0&a=tri\
pleplay4us&mr=0" width="130" height="86" alt="Ilhan Omar GOP challenger banned from Twitter after sayingshe should be &quot;tried for treason and hanged”"\
align="left" title="Ilhan Omar GOP challenger bannedfrom Twitter after saying she should be &quot;tried for treason and hanged”" border="0">\
</a>Danielle Stella campaign account also tweeted a picture of a stick figure being hanged with a link to a blog post about her comments.<p><br clear="all">\
'''
        html_result = '''Danielle Stella campaign account also tweeted a picture of a stick figure being hanged with a link to a blog post about her comments.'''
        self.assertEqual(rss_example.parse_html(html_example), html_result)

    def test_get_cached_news(self):
        rss_example1 = RSSReader('source', None, datetime(2019, 12, 1).date(), True, {}, False, 'tests/data_for_testing/news')
        rss_example2 = RSSReader('source', 1, datetime(2019, 12, 1).date(), False, {}, False, 'tests/data_for_testing/news')
        with open('tests/data_for_testing/all_news(date also 01-12-2019).txt', 'r') as f:
            all_news = f.read()
            rss_example1.get_cached_news()
            cached_news = ''
            for feed in rss_example1.news_to_print:
                cached_news += feed.__str__()
            self.assertEqual(all_news, cached_news)
        with open('tests/data_for_testing/one_news_from20191201.txt', 'r') as f:
            one_news = f.read()
            rss_example2.get_cached_news()
            cached_news = ''
            for feed in rss_example2.news_to_print:
                cached_news += feed.__str__()
            self.assertEqual(one_news, cached_news)

    def test_get_all_news(self):
        rss_example = RSSReader('source', None, datetime(2019, 12, 1).date(), True, {}, True, 'tests/data_for_testing/news')
        with open('tests/data_for_testing/all_news(date also 01-12-2019).txt', 'r') as f:
            all_news = f.read()
            rss_example.get_all_news()
            cached_news = ''
            for feed in rss_example.news_to_print:
                cached_news += feed.__str__()
            self.assertEqual(all_news, cached_news)

    def test_get_news(self):
        news = RSSReader.get_news(r'tests/data_for_testing/example_of_rss.xml')
        self.assertEqual(news.feed.title, 'Yahoo News - Latest News & Headlines')
        self.assertEqual(news.feed.link, 'https://www.yahoo.com/news')
        self.assertEqual(news.feed.subtitle, 'The latest news and headlines from Yahoo! News. Get breaking news stories and in-depth coverage with videos and photos.')
        self.assertEqual(news.feed.rights, 'Copyright (c) 2019 Yahoo! Inc. All rights reserved')
                
                
if __name__ == '__main__':
    unittest.main()
