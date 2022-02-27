from requests import get
import pandas as pd
from datetime import datetime
import datetime as dt
import time


class GetCandles:
    def __init__(self, symbol, interval, limit):
        self.symbol = symbol
        self.interval = interval
        self.limit = limit
        self.last_index = 0
        self.startTime = None
        self.df_last_candles = pd.DataFrame({
            "volume": [],
            "high": [],
            "low": [],
            "openTime": [],
            "open": [],
            "closeTime": [],
            "close": [],
        })
        self.date_now = datetime.now().strftime("%Y-%m-%d_%Hh")
        self.feed_1_more_time_ = True

    def get_starttime(self):
        if self.startTime is None:
            # Open Excel file
            df_excel_file = pd.read_excel("VET_rsi_with_ema.xlsx", sheet_name="15m")
            # Index column
            self.last_index = df_excel_file["id"].iloc[-1] + 1
            # startTime value
            # date_starttime = datetime.strptime(df_excel_file["closeTime"].iloc[-1], "%Y-%m-%d %H:%M:%S.%f")   This line converts string to datetime
            date_starttime = df_excel_file["closetime"].iloc[-1]
            self.startTime = int(time.mktime(date_starttime.timetuple())*1000)
        else:
            # startTime value
            date_starttime = self.df_last_candles["closeTime"].iloc[-1]
            self.startTime = int(time.mktime(date_starttime.timetuple()) * 1000)

    def get_data(self):
        """This method return a list from Binance API"""
        self.get_starttime()
        base_url = "https://api2.binance.com/api/v3/klines"
        params = f"?symbol={self.symbol}USDT&interval={self.interval}&limit={self.limit}&startTime={self.startTime}"
        url = base_url + params
        return get(url=url).json()

    def feed_dataframe(self, answer):
        for period in answer:
            self.df_last_candles = self.df_last_candles.append(
                pd.Series({
                    "volume": period[5],
                    "high": period[2],
                    "low": period[3],
                    "openTime": period[0],
                    "open": period[1],
                    "closeTime": period[6],
                    "close": period[4],
                }),
                ignore_index=True)

    def feed_1_more_time(self):
        last_close_time = self.df_last_candles["closeTime"].iloc[-1]
        if last_close_time + dt.timedelta(minutes=15) > datetime.now():
            self.feed_1_more_time_ = False

    def insert_index_column(self):
        list_index = [i for i in range(self.last_index, self.last_index + self.df_last_candles.shape[0])]
        self.df_last_candles.insert(0, "id", list_index)

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

    def export_new_candles_to_excel(self):
        while self.feed_1_more_time_:
            answer = self.get_data()
            answer = self.change_datetime_format(answer)
            self.feed_dataframe(answer)
            self.feed_1_more_time()
        self.insert_index_column()
        self.df_last_candles.to_excel(f"{self.symbol}_{self.date_now}.xlsx", index=False)


getter = GetCandles(
    symbol="VET",
    interval="15m",
    limit="1000"
)
getter.export_new_candles_to_excel()
