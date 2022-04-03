import pandas as pd
from sqlalchemy import create_engine
from dataclasses import dataclass
import logging

from src.strategies.rsi.DecisionRules import search_candle_to_buy
from src.utils.tools import Candle, PreviousPositions

logging.basicConfig(format="%(asctime)s %(message)s", datefmt="%Y/%m/%d %H:%M:%S")


@dataclass
class Action:
    """
    This class is used to check if there is a buy or sell action to make. If there is, the CryptoBot will buy
    and/or sell crypto on Binance.
    """
    symbol: str
    candle_to_buy = Candle()
    candle_trigger = Candle()
    candles_tail = pd.DataFrame()
    previous_position = PreviousPositions()

    def candle_to_buy_is_the_last_candle(self):
        print("wait")
        if self.candle_to_buy.closetime == self.candle_trigger.opentime:
            return True
        else:
            return False

    def run(self, candles):
        previous_positions = PreviousPositions(self.symbol)
        self.buying_signal(candles, previous_positions)
        self.selling_signal(candles, previous_positions)

    def buying_signal(self, candles, previous_positions):
        self.candle_to_buy, self.candle_trigger, self.candles_tail = search_candle_to_buy(candles)
        opened_positions = previous_positions.df.opened_positions

        if self.candle_to_buy.opentime not in opened_positions and self.candle_to_buy_is_the_last_candle():
            self.buy()
            self.create_new_position()
            self.records_buying_movements()
        else:
            logging.info(f"\n{self.symbol} | Nothing bought.\n")

    def buy(self):
        pass

    def create_new_position(self):
        self.opentime_trigger_candle = candles_trigger["opentime"]
        self.opentime_buying_candle = candle_to_buy["opentime"]
        self.buying_timestamp = ... # ça dépend de la réponse de Binance. L'api doit nous confirmer l'achat
        self.buying_price = ... # ça dépend de Binance
        self.target_sales_price = ... # ça dépend de Binance
        self.bet = 50
        self.crypto_quantity = ... # ça dépend de Binance
        logging.info("New position created""")

    def records_buying_movements(self):
        """This method records buying position in the DB"""
        # poseidon <=> The engine
        db_uri = "sqlite:///../poseidon.db"
        poseidon = create_engine(db_uri, echo=True)
        tb_name = f"{self.symbol}_opened_positions"

        df_position = self.create_df_buying_position()

        # Insert position in Sql database
        df_position.to_sql(tb_name, con=poseidon, if_exists="append", index=False)

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

    def selling_signal(self, candles, previous_positions):
        return False

    def sell(self):
        pass

    def records_selling_movements(self):
        """This method records buying position in the DB"""
        # poseidon <=> The engine
        db_uri = "sqlite:///../poseidon.db"
        poseidon = create_engine(db_uri, echo=True)
        tb_name = f"{self.symbol}_closed_positions"

        df_position = self.create_df_selling_position()

        # Insert position in Sql database
        df_position.to_sql(tb_name, con=poseidon, if_exists="append", index=False)

    def create_df_selling_position(self) -> pd.DataFrame:
        return
