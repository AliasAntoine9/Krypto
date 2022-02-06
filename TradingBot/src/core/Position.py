from datetime import datetime
import pandas as pd
from sqlalchemy import create_engine
from dataclasses import dataclass

from TradingBot.src.strategies.rsi.DecisionRules import search_candle_to_buy
from TradingBot.src.utils.KryptoProperties import KryptoProperties


class Position:

    def __init__(self, symbol):
        self.symbol = symbol
        self.opentime_candle_trigger = ""
        self.opentime_candle_to_buy = ""
        self.buy_timestamp = ""
        self.price = 0
        self.price_to_sale = 0
        self.bet = 0
        self.crypto_quantity = 0

    def candle_to_buy_is_the_last_candle(self, df_tail):
        last_row = df_tail.last_valid_index()
        if df_tail["closetime"][last_row] == self.opentime_candle_trigger:
            return True
        else:
            return False

    def take_position_if_new(self, df_candles, previous_positions):
        self.opentime_candle_to_buy, self.opentime_candle_trigger, df_tail = search_candle_to_buy(df=df_candles)
        candle_to_buy = self.opentime_candle_to_buy
        opened_positions = previous_positions.df.opened_positions

        if candle_to_buy not in opened_positions and self.candle_to_buy_is_the_last_candle(df_tail):
            self.buy()
            self.create_new_position()
            print(f"""Time: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}  |  New position created""")

    def run(self, df_candles):
        previous_position = PreviousPositions(self.symbol)
        self.take_position_if_new(df_candles=df_candles, previous_positions=previous_position)

    def buy(self):
        pass

    def sold(self):
        pass

    def create_new_position(self):
        self.buy_timestamp = ...
        self.price = ...
        self.price_to_sale = ...
        self.bet = ...
        self.crypto_quantity = ...
        self.insert_new_position_in_sql()

    def insert_new_position_in_sql(self):
        # poseidon <=> The engine
        db_uri = "sqlite:///../poseidon.db"
        poseidon = create_engine(db_uri, echo=True)
        tb_name = "opened_positions"

        df_position = self.create_df_position()

        # Insert position in Sql database
        df_position.to_sql(tb_name, con=poseidon, if_exists="append", index=False)

    def create_df_position(self):
        df_position = pd.DataFrame(
            {
                "opentime_candle_trigger": [self.opentime_candle_trigger],
                "opentime_candle_to_buy": [self.opentime_candle_to_buy],
                "buy_timestamp": [self.buy_timestamp],
                "price": [self.price],
                "price_to_sale": [self.price * 1.02],
                "bet": [self.bet],
                "crypto_quantity": [self.crypto_quantity],
            }
        )
        return df_position


class PreviousPositions:
    """Get previous positions for 1 symbol (crypto)"""

    @dataclass
    class Dataframe:
        positions = pd.DataFrame()

    def __init__(self, symbol):
        self.symbol = symbol
        self.df = self.Dataframe()
        self.db_uri = KryptoProperties.db_url
        self.get_positions("opened")
        self.get_positions("closed")

    def get_positions(self, status):
        """This method allows to get the opened position for 1 symbol"""
        # poseidon <=> The engine

        poseidon = create_engine(self.db_uri, echo=True)
        tb_name = f"{self.symbol}_{status}_positions"

        self.df.positions = pd.read_sql_table(
            table_name=tb_name,
            con=poseidon
        )
