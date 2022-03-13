from datetime import datetime
import pandas as pd
from sqlalchemy import create_engine
from dataclasses import dataclass

from TradingBot.src.strategies.rsi.DecisionRules import search_candle_to_buy
from TradingBot.src.utils.KryptoProperties import KryptoProperties


@dataclass
class Position:
    opentime_trigger_candle: str
    opentime_buying_candle: str
    buying_timestamp: str
    buying_price: float
    target_sales_price: float
    bet: float
    crypto_quantity: float

    def __init__(self, symbol):
        self.symbol = symbol

    def candle_to_buy_is_the_last_candle(self, candles_tail):
        last_row = candles_tail.last_valid_index()
        if candles_tail["closetime"][last_row] == self.opentime_trigger_candle:
            return True
        else:
            return False

    def take_position_if_new(self, candles, previous_positions):
        self.opentime_buying_candle, self.opentime_trigger_candle, candles_tail = search_candle_to_buy(candles)
        candle_to_buy = self.opentime_buying_candle
        opened_positions = previous_positions.df.opened_positions

        if candle_to_buy not in opened_positions and self.candle_to_buy_is_the_last_candle(candles_tail):
            self.buy()
            self.create_new_position()
            print(f"""Time: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}  |  New position created""")
        else:
            print("\nNo VET bought. Waiting for the good moment...\n")

    def run(self, candles):
        previous_position = PreviousPositions(self.symbol)
        self.take_position_if_new(candles, previous_position)

    def buy(self):
        pass

    def sold(self):
        pass

    def create_new_position(self):
        self.opentime_trigger_candle = ...
        self.opentime_buying_candle = ...
        self.buying_timestamp = ...
        self.buying_price = ...
        self.target_sales_price = ...
        self.bet = ...
        self.crypto_quantity = ...
        self.insert_new_position_in_sql()

    def insert_new_position_in_sql(self):
        # poseidon <=> The engine
        db_uri = "sqlite:///../poseidon.db"
        poseidon = create_engine(db_uri, echo=True)
        tb_name = f"{self.symbol}_opened_positions"

        df_position = self.create_df_position()

        # Insert position in Sql database
        df_position.to_sql(tb_name, con=poseidon, if_exists="append", index=False)

    def create_df_position(self):
        new_position = pd.DataFrame(
            {
                "opentime_trigger_candle": [self.opentime_trigger_candle],
                "opentime_buying_candle": [self.opentime_buying_candle],
                "buying_timestamp": [self.buying_timestamp],
                "buying_price": [self.buying_price],
                "target_sales_price": [self.buying_price * 1.02],
                "bet": [self.bet],
                "crypto_quantity": [self.crypto_quantity],
            }
        )
        return new_position


class PreviousPositions:
    """Get previous positions for 1 symbol (crypto)"""

    @dataclass
    class Dataframe:
        opened_positions = pd.DataFrame()
        closed_positions = pd.DataFrame()

    def __init__(self, symbol):
        self.symbol = symbol
        self.df = self.Dataframe()
        self.db_uri = KryptoProperties.db_url
        self.get_positions()

    def get_positions(self):
        """This method allows to get the opened position for 1 symbol"""
        # poseidon <=> The engine

        for status in ("opened", "closed"):
            poseidon = create_engine(self.db_uri, echo=True)
            tb_name = f"{self.symbol}_{status}_positions"

            positions = pd.read_sql_table(
                table_name=tb_name,
                con=poseidon
            )

            setattr(self.df, f"{status}_positions", positions)
