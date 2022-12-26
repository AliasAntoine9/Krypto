import unittest
from src.scrapping.rest_api_scrapper import RestApiScrapper

class TestScrapper(unittest.TestCase):
	"""This class is a first try to implement unit tests"""

	def setUp(self):
		"""Setup the testing environment by creating instances objects used by all test methods."""
		print("Avant le test")
		scrapper = RestApiScrapper("VET")
	
	def test_get_candles_return_json(self):
		"""test_get_candles_return_json"""
		return

	def tearDown(self):
		"""
		Clean the test environnement by deleting outputs (like files), disconnect database connect setup, ...
		This is usefull to keep test environnement clean like that we can immediatly run a new bunch of test !
		"""
		print("Après le test")

if __name__ == "__main__":
	unittest.main()