import pandas as pd
from sqlalchemy import create_engine
import logging

from src.strategies.rsi.decision_rules import search_candle_to_buy
from src.utils.tools import Candle, Position, PreviousPositions

logging.basicConfig(format="%(asctime)s %(message)s", datefmt="%Y/%m/%d %H:%M:%S")


class Action:
    """
    This class is used to check if there is a buy or sell action to make. If there is, the CryptoBot will buy
    and/or sell crypto on Binance.
    """
    def __init__(self, symbol, candles):
        self.symbol = symbol
        self.candles = candles
        self.candle_to_buy = Candle()
        self.candle_trigger = Candle()
        self.candles_tail = pd.DataFrame()
        self.previous_positions = PreviousPositions(self.symbol)

    def candle_to_buy_is_the_last_candle(self):
        print("wait")
        if self.candle_to_buy.closetime == self.candle_trigger.opentime:
            return True
        else:
            return False

    def run(self):
        self.search_buying_signal()
        self.search_selling_signal()

    def search_buying_signal(self):
        self.candle_to_buy, self.candle_trigger, self.candles_tail = search_candle_to_buy(self.candles)
        opened_positions = self.previous_positions.df.opened_positions

        if self.candle_to_buy.opentime not in opened_positions["opentime_buying_candle"]\
                and self.candle_to_buy_is_the_last_candle():
            self.buy()
            self.records_buying_movements()
        else:
            logging.info(f"\n{self.symbol} | Nothing bought.\n")

    def buy(self):
        # Make the buy order on Binance

        # Save buying order by creating a new opened position
        position = Position(
            symbol=self.symbol,
            opentime_buying_candle="",
            buying_timestamp="",
            buying_price=0.0,
            target_sales_price=0.0,
            bet=50.0,
            crypto_quantity=0.0
        )
        return

    def records_buying_movements(self):
        """This method records buying position in the DB"""
        # ploutos <=> The engine
        db_uri = "sqlite:///ploutos.db"
        ploutos = create_engine(db_uri, echo=True)
        tb_name = f"{self.symbol}_opened_positions"

        df_position = self.create_df_buying_position()

        # Insert position in Sql database
        df_position.to_sql(tb_name, con=ploutos, if_exists="append", index=False)
        logging.info("New position created")

    def create_df_buying_position(self):
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

    def search_selling_signal(self):
        return

    def sell(self):
        pass

    def records_selling_movements(self):
        """This method records buying position in the DB"""
        # ploutos <=> The engine
        db_uri = "sqlite:///ploutos.db"
        ploutos = create_engine(db_uri, echo=True)
        tb_name = f"{self.symbol}_closed_positions"

        df_position = self.create_df_selling_position()

        # Insert position in Sql database
        df_position.to_sql(tb_name, con=ploutos, if_exists="append", index=False)

    def create_df_selling_position(self) -> pd.DataFrame:
        return
