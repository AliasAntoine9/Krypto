import unittest
from src.scrapping.rest_api_scrapper import RestApiScrapper

class TestScrapper(unittest.TestCase):
	"""This class is a first try to implement unit tests"""

	def setUp(self):
		"""Arrange environment"""
		print("Avant le test")
		scrapper = RestApiScrapper("VET")
	
	def test_get_candles_return_json(self):
		"""test_get_candles_return_json"""
		return

	def tearDown(self):
		"""Assert everything goes well"""
		print("Après le test")

if __name__ == "__main__":
	unittest.main()