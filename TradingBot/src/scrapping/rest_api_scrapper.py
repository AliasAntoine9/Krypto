from requests import get
from datetime import datetime


class RestApiScrapper:
    def __init__(self, symbol):
        self.symbol = symbol
        self.timestamp = datetime.now().strftime("%Y-%m-%d_%Hh")

    def get_candles(self):
        """This method return a list from Binance API"""
        base_url = "https://api2.binance.com/api/v3/klines"
        params = f"?symbol={self.symbol.upper()}USDT&interval=15m&limit=1000"
        url = base_url + params
        return get(url=url)
