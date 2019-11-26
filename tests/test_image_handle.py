"""Tests must be called from root project's directory."""
import unittest
import sys, os

import requests

sys.path.append(os.getcwd() + '/rssreader')

from rss_reader.image_handle import *


CORRECT_IMG_LINK = 'http://l2.yimg.com/uu/api/res/1.2/IxBCyyfTvHOinsGnZblALA--\
/YXBwaWQ9eXRhY2h5b247aD04Njt3PTEzMDs-/https://media.zenfs.com/en/ap.org/bf010b612afa709627612729a5bad605'

INCORRECT_IMG_LINK = 'qwerty'


class TestImageHandle(unittest.TestCase):
	
	def setUp(self):
		pass


	def tearDown(self):
		pass


	def test_save_image_by_url(self):
		try:
			save_image_by_url(INCORRECT_IMG_LINK, '')
		except Exception as exception:
			self.assertEqual(type(exception), requests.exceptions.MissingSchema)


	def test_get_image_as_base64(self):
		encoding_str = get_image_as_base64(CORRECT_IMG_LINK)
		self.assertIsNotNone(encoding_str)
		self.assertIsNotNone(base64.b64decode(encoding_str))


if __name__ == '__main__':
	unittest.main()