from requests import get
import pandas as pd
from datetime import datetime


class ParseMarketData:
    def __init__(self, symbol):
        self.symbol = symbol
        self.df_close = pd.DataFrame({
            "closeTime": [],
            "close": [],
            "openTime": [],
            "open": [],
            "high": [],
            "low": [],
            "volume": []
        })
        self.timestamp = datetime.now().strftime("%Y-%m-%d_%Hh")

    def get_data(self):
        """This method return a list from Binance API"""
        base_url = "https://api2.binance.com/api/v3/klines"
        params = f"?symbol={self.symbol}USDT&interval=15m&limit=1000"
        url = base_url + params
        return get(url=url).json()

    def feed_dataframe(self, answer):
        for period in answer:
            self.df_close = self.df_close.append(
                pd.Series({
                    "closeTime": period[6],
                    "close": period[4],
                    "openTime": period[0],
                    "open": period[1],
                    "high": period[2],
                    "low": period[3],
                    "volume": period[5]
                }),
                ignore_index=True)

    @staticmethod
    def change_datetime_format(list_answers):
        for period in list_answers:
            # Period[i] is a MillisecondsUnixTimestamp string
            # 1st -> Convert the string period[i] to int
            # 2nd -> Convert MillisecondsUnixTimestamp to UnixTimeStamp
            # 3rd -> Convert UnixTimestamp to string well formatted
            str_openTime_formatted = datetime.fromtimestamp(int(period[0])/1000).strftime("%Y-%m-%d %H:%M:%S")
            str_closeTime_formatted = datetime.strftime(datetime.fromtimestamp(int(period[6]) / 1000),
                                                        "%Y-%m-%d %H:%M:%S")

            # Convert string to datetime64 format
            period[0] = datetime.strptime(str_openTime_formatted, "%Y-%m-%d %H:%M:%S")
            period[6] = datetime.strptime(str_closeTime_formatted, "%Y-%m-%d %H:%M:%S")
        return list_answers

    def create_dataframe(self):
        answer = self.get_data()
        answer = self.change_datetime_format(answer)
        self.feed_dataframe(answer)
        # self.df_close.to_csv(f"{self.symbol}_close_{self.timestamp}.csv", index=False)
        return self.df_close


# 1 period is:
# openTime - 0
# open - 1
# high - 2
# low - 3
# close - 4
# volume - 5
# closeTime - 6
# quoteAssetVolume - 7
# numberOfTrades - 8
# takerBuyBaseAssetVolume - 9
# takerBuyQuoteAssetVolume - 10
# ignore - 11
#
# UnixTimeStamp: 1636722000
