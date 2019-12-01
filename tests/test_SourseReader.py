
'''
Tests fore SourseReader.NewsReader module
'''
import unittest
import feedparser
import os
import json
from datetime import datetime

from PythonHomework.SourseReader import NewsReader

correct_link = 'https://news.yahoo.com/rss/'
incorrect_link = 'https://news.yahoo.com'

class NewsREaderTestCase(unittest.TestCase):
    '''
    Test cases for NewsReader class
    '''
    def setUp(self) -> None:
        '''Take correct rss file from filesystem'''
        with open('correct_rss.rss','r') as rf:
            self.read = rf.read()        

    def test_check_internet(self):
        pass
        

    def test_parse_rss(self):
        wd = os.getcwd()
        list_news = [{'title': 'Stranger Sings', 'feed': 'Some sort of sourse', 'date': '2019-10-31T11:42:00Z', 'simple_date': 20191031, 'link': 'https://strange.news.by/strange/1.html', 'description': 'The sun is shining', 'image': 'https://img.strange.by/n/reuters/0c/a/secret_1.jpg', 'links': 'https://strange.news.by/strange/1.html\n\t'}, {'title': 'Birds', 'feed': 'Some sort of sourse', 'date': '2019-10-31T15:42:00Z', 'simple_date': 20191031, 'link': 'https://strange.news.by/strange/2.html', 'description': 'The birds are signing', 'image': 'https://img.strange.by/n/reuters/0c/a/secret_2.jpg', 'links': 'https://strange.news.by/strange/2.html\n\t'}, {'title': 'Animals', 'feed': 'Some sort of sourse', 'date': '2019-10-29T11:42:00Z', 'simple_date': 20191029, 'link': 'https://strange.news.by/strange/3.html', 'description': 'The animals are jumping', 'image': 'https://img.strange.by/n/reuters/0c/a/secret_3.jpg', 'links': 'https://strange.news.by/strange/3.html\n\t'}]
        self.newslist = NewsReader(self.read).parse_rss()
        self.assertEqual(self.newslist,list_news)

    def test_desc_of_resourse(self):

        self.rss = feedparser.parse(self.read)
        test_tuple = ('Some sort of sourse','https://strange.news.by/','No image')
        try:
            image = str(self.rss.feed.image.url)
        except AttributeError:
            image = 'No image'
        title = str(self.rss.feed.title)
        link = str(self.rss.feed.link)
        desc_tuple =(title,link,image)
        self.assertEqual(test_tuple,desc_tuple)
                    
    def test_make_json(self):
        json_test = NewsReader(self.read).make_json()
        # Checking for symbols equality
        len_json = 382
        self.assertEqual(len(json_test[0]),len_json)

        len_json_2 = 376
        self.assertEqual(len(json_test[1]),len_json_2)

        len_json_3 = 380
        self.assertEqual(len(json_test[2]),len_json_3)

    def test_json_for_html(self):
        json_test = NewsReader(self.read).json_for_html()
        len_json = 418 
        self.assertEqual(len(json_test[0]),len_json)

    def test_make_html(self):
        pass

    def test_print_rss(self):
        pass



if __name__ == '__main__':
   unittest.main()