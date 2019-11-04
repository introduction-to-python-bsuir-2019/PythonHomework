import unittest
import datetime

from rss_reader import NewsReader


class TestNewsReader(unittest.TestCase):
    def setUp(self) -> None:
        self.feed = NewsReader(url='no url')

        self.feed.items = {'title': 'CNN.com - RSS Channel - World',
                           0: {'title': "New Delhi is choking on smog and there's no end in sight", 'pubDate': 'Mon, 04 Nov 2019 09:59:11 GMT', 'link': 'http://rss.cnn.com/~r/rss/edition_world/~3/tbjRLXCRMIE/index.html', 'description': "• Air pollution reaches 'unbearable' levels", 'imageLink': 'http://feeds.feedburner.com/~r/rss/edition_world/~4/tbjRLXCRMIE', 'imageDescription': ''},
                           1: {'title': "World's most profitable company to IPO", 'pubDate': 'Mon, 04 Nov 2019 10:43:39 GMT', 'link': 'http://rss.cnn.com/~r/rss/edition_world/~3/WdGBNzqr0Ko/index.html', 'description': '', 'imageLink': 'http://feeds.feedburner.com/~r/rss/edition_world/~4/WdGBNzqr0Ko', 'imageDescription': ''},
                           2: {'title': 'China perfected fake meat centuries before the Impossible Burger', 'pubDate': 'Mon, 04 Nov 2019 09:19:17 GMT', 'link': 'http://rss.cnn.com/~r/rss/edition_world/~3/gb96p9WE7ow/index.html', 'description': '', 'imageLink': 'http://feeds.feedburner.com/~r/rss/edition_world/~4/gb96p9WE7ow', 'imageDescription': ''},
                           3: {'title': 'Why US military aid is so crucial to Ukraine', 'pubDate': 'Mon, 04 Nov 2019 02:48:34 GMT', 'link': 'http://rss.cnn.com/~r/rss/edition_world/~3/YxPYqk6S_S4/ukraine-troops-front-lines-russia-ward-pkg-vpx.cnn', 'description': "Following the now infamous phone call between President Trump and Ukrainian President Volodymyr Zelensky, the US temporarily suspended nearly $400 million in military and security aid to Ukraine. CNN's Clarissa Ward reports from the front lines of Ukraine's war with Russia, where forces say the need for military aid is dire.", 'imageLink': 'http://feeds.feedburner.com/~r/rss/edition_world/~4/YxPYqk6S_S4', 'imageDescription': ''},
                           4: {'title': "China approves seaweed-based Alzheimer's drug. It's the first new one in 17 years", 'pubDate': 'Mon, 04 Nov 2019 07:55:31 GMT', 'link': 'http://rss.cnn.com/~r/rss/edition_world/~3/egUv2keeyj8/index.html', 'description': "Authorities in China have approved a drug for the treatment of Alzheimer's disease, the first new medicine with the potential to treat the cognitive disorder in 17 years.", 'imageLink': 'http://feeds.feedburner.com/~r/rss/edition_world/~4/egUv2keeyj8', 'imageDescription': ''},
                           5: {'title': 'One year after the Google walkout, key organizers reflect on the risk to their careers', 'pubDate': 'Fri, 01 Nov 2019 20:42:24 GMT', 'link': 'http://rss.cnn.com/~r/rss/edition_world/~3/7xztEBsGMGk/index.html', 'description': 'Claire Stapleton and Meredith Whittaker staked their careers when they organized the Google walkout in November 2018. It was a risk they felt they had to take.', 'imageLink': 'http://feeds.feedburner.com/~r/rss/edition_world/~4/7xztEBsGMGk', 'imageDescription': ''},
                           6: {'title': 'Tech stocks rally in Asia after news that a Huawei reprieve could come soon', 'pubDate': 'Mon, 04 Nov 2019 10:57:36 GMT', 'link': 'http://rss.cnn.com/~r/rss/edition_world/~3/RzbapX1NKyg/index.html', 'description': "Asian markets edged up on Monday, following last week's gains on Wall Street as well as news of a potential reprieve for Huawei.", 'imageLink': 'http://feeds.feedburner.com/~r/rss/edition_world/~4/RzbapX1NKyg', 'imageDescription': ''},
                           7: {'title': "They're recycling plastic milk bottles to build roads", 'pubDate': 'Wed, 30 Oct 2019 10:28:31 GMT', 'link': 'http://rss.cnn.com/~r/rss/edition_world/~3/nkb1bSv3X-M/index.html', 'description': 'Plastic milk bottles are being recycled to make roads in South Africa, with the hope of helping the country tackle its waste problem and improve the quality of its roads.', 'imageLink': 'http://feeds.feedburner.com/~r/rss/edition_world/~4/nkb1bSv3X-M', 'imageDescription': ''},
                           8: {'title': "Russia rolls out its 'sovereign internet'", 'pubDate': 'Fri, 01 Nov 2019 16:21:25 GMT', 'link': 'http://rss.cnn.com/~r/rss/edition_world/~3/vztqGYJG8oY/index.html', 'description': 'On Friday, a controversial new law took effect in Russia: The so-called "sovereign internet" law, which mandates the creation of an independent internet for Russia.', 'imageLink': 'http://feeds.feedburner.com/~r/rss/edition_world/~4/vztqGYJG8oY', 'imageDescription': ''},
                           9: {'title': "US cities are losing 36 million trees a year. Here's why it matters ", 'pubDate': 'Wed, 18 Sep 2019 16:44:32 GMT', 'link': 'http://rss.cnn.com/~r/rss/edition_world/~3/KlnsnygiAw8/index.html', 'description': "<i>If you're looking for a reason to care about tree loss, the nation's latest heat wave might be it.  Trees can lower summer daytime temperatures by as much as 10 degrees Fahrenheit, according to a recent study.</i>", 'imageLink': 'http://feeds.feedburner.com/~r/rss/edition_world/~4/KlnsnygiAw8', 'imageDescription': ''}}

    def test_get_date(self):
        date_0 = str(self.feed.get_date(self.feed.items[0]['pubDate']))
        res_date_0 = str(datetime.datetime.today().date())
        self.assertEqual(date_0, res_date_0)

        date_1 = str(self.feed.get_date(self.feed.items[1]['pubDate']))
        res_date_1 = '2019-11-04'
        self.assertEqual(date_1, res_date_1)

        date_7 = str(self.feed.get_date(self.feed.items[7]['pubDate']))
        res_date_7 = '2019-10-30'
        self.assertEqual(date_7, res_date_7)

    def test_get_description(self):
        description_0 = self.feed.get_description(self.feed.items[0]['description'])
        res_description_0 = '• Air pollution reaches \'unbearable\' levels'
        self.assertEqual(description_0, res_description_0)

        description_1 = self.feed.get_description(self.feed.items[1]['description'])
        res_description_1 = ''
        self.assertEqual(description_1, res_description_1)

        description_9 = self.feed.get_description(self.feed.items[9]['description'])
        res_description_9 = 'If you\'re looking for a reason to care about tree loss, ' \
                            'the nation\'s latest heat wave might be it.  Trees can ' \
                            'lower summer daytime temperatures by as much as 10 degrees ' \
                            'Fahrenheit, according to a recent study.'
        self.assertEqual(description_9, res_description_9)


if __name__ == '__main__':
    unittest.main()
