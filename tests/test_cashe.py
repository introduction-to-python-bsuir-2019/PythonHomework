'''
Test for cashing module
'''

from unittest import TestCase
from unittest.mock import patch,call,Mock
from PythonHomework.cash import StoreCashSql
from PythonHomework.SourseReader import NewsReader

class CashTestCase(TestCase):

	def setUp(self):
		self.mock_cash = Mock(db='fake/db')
		self.mock_connection = Mock()
		self.moch_connection.__str__ = Mock(return_value=self.mock_cash.db)
		self.mock_connection.cursor = Mock()

	def test__init(self):
		pass

	def test_create_db(self):
		with patch('sqlite3.connect',return_value=self.mock_connection):
			StoreCashSql.create_db(self.mock_cash)

		self.assertEqual(self.mock_cach.db, self.mock_connection.__str__())
		self.mock_connection.cursor.assert_called()

