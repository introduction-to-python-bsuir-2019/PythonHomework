import unittest
import argparse
from rss_reader import news
from rss_reader.rss_fb2 import encode_image
from rss_reader import arg

class handlers(unittest.TestCase):

	def test_clean_text(self):
		test_string = "<sofnfroia>Test</a>"
		self.assertEqual(news.clean_text(test_string), "Test")
		
	def test_text_searching(self):
		text_example = '<p><a href="https://news.yahoo.com/fire-kills-unknown-number-animals-031907022.html"><img src="http://l1.yimg.com/uu/api/res/1.2/0t6.FgqWA_rRrbNwiFuHBA--/YXBwaWQ9eXRhY2h5b247aD04Njt3PTEzMDs-/https://media.zenfs.com/en-us/usa_today_news_641/47ee38aeea6311069963e8976e56fdfe" width="130" height="86" alt="Giraffes among 10 animals killed in &#39;tragic&#39; Ohio safari wildlife park fire" align="left" title="Giraffes among 10 animals killed in &#39;tragic&#39; Ohio safari wildlife park fire" border="0" ></a>Test description<p><br clear="all">'
		self.assertEqual(news.get_Text(text_example), "Test description")

	def test_encode(self):
		encoded_image_example = "/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAAgGBgcGBQgHBwcJCQgKDBQNDAsLDBkSEw8UHRofHh0aHBwgJC4nICIsIxwcKDcpLDAxNDQ0Hyc5PTgyPC4zNDL/2wBDAQkJCQwLDBgNDRgyIRwhMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjL/wgARCAAwAEgDASIAAhEBAxEB/8QAGgAAAgMBAQAAAAAAAAAAAAAAAAQCAwUGAf/EABkBAAMBAQEAAAAAAAAAAAAAAAACAwEEBf/aAAwDAQACEAMQAAABXkX+d0Ikpmr7ufatZ0OrrmMRKJFvF0+melrZvQSOaR6fyPTGlihV58fLzxXslmyd/LldSJaWUm2eVmAemH//xAAkEAACAgICAQMFAAAAAAAAAAABAgADBBESIRMFECIUJDEyNP/aAAgBAQABBQL1AfesvWprcSs2ZAx0LW0mqEDxVnb5395+fsiGw/rK7yCb0uSzf0tP4a92AtZZ2xUeOh+gp+dCcFzW44q6WWg8xWd1h1ldFgULXcoxcZDWeMuTzQ4iy5QXxsgrKcephbfptCanc79tgt0QmdfXX6atbS9+Vs3qcpuf/8QAGREAAgMBAAAAAAAAAAAAAAAAARAAAhES/9oACAEDAQE/AUKTlagZYzp6X//EAB0RAAICAwADAAAAAAAAAAAAAAABAhEQEiExQVH/2gAIAQIBAT8B9LEsM1RIcqIrvSoj8Ua/Sln/xAAmEAABAwIGAgIDAAAAAAAAAAABAAIRIUEDEBIiMVEycRSRIEJi/9oACAEBAAY/AmevwEWUFzlMyEHTVFYfoKlsoCAHLrrSf1Nk9jdzggSLqVvgu7KaG3upKdpbMqtlqF1tj+lDrlQ3U4dwq9qYotcktHKc557p0t1FrDK+1iNEwaglbxx2vBq5QwsRupq1D6Rw217y8iuc9x+lQOhCBUXhfIxDGISUY0wuAuM//8QAIRABAAICAgIDAQEAAAAAAAAAAQARITFBYVGBcZGxwfD/2gAIAQEAAT8hRA5H7FpLMwVAlU7LxMhKthiNcLhgLq/EtPcdN4/SY2mRbL2VHm0LXqVR1blLQF/ShAIbqoSW7fBBl2l+WL5fUeoOiJ20pfuMk1mwF48iXNKGY3zDetto5YOOKDHEJI8Q7QBMaiqv8VxKSzgPNXxLBzkcYtNVXupkQOcqbZdg9SjQ1oZSriOlD4ipCuFhQLPLRFwUYU+X0Qp/Uid3qaxf9U2AwcYOPMz9F6IBW5VW/JBt6MY5g3/COxj3naf/2gAMAwEAAgADAAAAEC3PMwXp9q/oLVSvP//EABoRAAMAAwEAAAAAAAAAAAAAAAABERAhMVH/2gAIAQMBAT8QXMKaHFpC3oTnTxE7K8IrRilLn//EABsRAQEBAQEAAwAAAAAAAAAAAAEAESExEEFR/9oACAECAQE/EFY3bSaRudj2DNyP4QBH2VL4teq32LR2adyT4//EACQQAQACAgIBBAIDAAAAAAAAAAEAESExQVFxYYGRsaHh0fDx/9oACAEBAAE/EDEbhB8lNuo1g0OWWyrTScw5oR0j6x63mBxU1i1NZ6hk3StVdarGvcjP05fcfvh+UXBAF1Zz8RQBleUhio/UAcrCrSLJlCashVY/1HXDzEE/bAwmgspTk9/qLjXaZUYUFeri0XCpilvetb5mnltEbTB1r9QBRnCnCt6AtqELDdVpf6xrAElzafzM/uVwOinuC8iFcFuqIF150Lur8wUA7gxMtSAWiuE6fMURCXZDQvAueMkVcpQBZb79SjeQKA+DHcbLwyjWbDuMQGZddGz8ntMPSFYDjZ0wdFIcFP3GoZ14UXK30cu/eKiQG+08SsjgJTsq8RYqyVVYK+ZxPQz1xiIcH4Ipo5PDEAKAOLQFSFztcNTGKNr6tYgMuVd16NbYsZACyGDY0rKiSZg05uUlsO5qYA6b2wsgUXi0jmAV8z//2Q=="
		self.assertEqual(encode_image("test_image.jpg"), encoded_image_example)

	def test_description(self):
		arg.args.date = "20191130"
		self.assertTrue(news.compare_dates("Sat, 30 Nov 2019 09:22:00 +0300"))

if __name__ == "__main__":
	unittest.main()

