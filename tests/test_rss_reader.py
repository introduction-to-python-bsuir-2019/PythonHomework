import unittest
from rss_reader.rss_reader import NewsReader

class TestNewsReader(unittest.TestCase):
    def test_parse_xml(self):
        computed_xml = "[{'title': 'Министр внутренних дел: Мы работаем не на показатели, а на граждан', 'date': 'Sun, 01 Dec 2019 21:06:00 +0300', 'text': 'МВД меняет подходы к наркопреступлениям, ставка будет на профилактику и на выявление крупных поставщиков, заявил в эфире программы «Контуры» телеканала ОНТ министр внутренних дел Юрий Караев.', 'link': 'https://news.tut.by/society/663397.html', 'hrefs': ['https://img.tyt.by/n/buryakina/01/7/karaev_20190410_bur_tutby_phsl-9055.jpg']}]"
        test_xml = """
{ 
    'title':'Министр внутренних дел: Мы работаем не на показатели, а на граждан',
    'link':'https://news.tut.by/society/663397.html?utm_campaign=news-feed&utm_medium=rss&utm_source=rss-news',
    'published':'Sun, 01 Dec 2019 21:06:00 +0300',
    'summary':'<img src="https://img.tyt.by/thumbnails/n/buryakina/01/7/karaev_20190410_bur_tutby_phsl-9055.jpg" width="72" height="48" alt="Фото: Дарья Бурякина, TUT.BY" border="0" align="left" hspace="5" />МВД меняет подходы к наркопреступлениям, ставка будет на профилактику и на выявление крупных поставщиков, заявил в эфире программы «Контуры» телеканала ОНТ министр внутренних дел Юрий Караев.<br clear="all" />',
    'media_content':[ 
         { 
            'url':'https://img.tyt.by/n/buryakina/01/7/karaev_20190410_bur_tutby_phsl-9055.jpg',
            'type':'image/jpeg',
            'medium':'image',
            'height':'800',
            'width':'1200',
            'filesize':'371255'
         }
    ]
}
"""
        self.assertEqual(NewsReader.parse_xml(test_xml), computed_xml)

    def test_clean_html_text(self):
        self.assertEqual(NewsReader.clean_html_text("Some&nbsp;String"), "SomeString")

if __name__ == '__main__':
    unittest.main()