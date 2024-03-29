from dataclasses import dataclass
import pandas as pd
from sqlalchemy import create_engine
from jproperties import Properties
from pathlib import Path


@dataclass
class DataFrame:
    candles = pd.DataFrame()
    candles_tail = pd.DataFrame()


@dataclass
class Candle:
    opentime: str = None
    open: float = None
    high: float = None
    low: float = None
    close: float = None
    volume: float = None
    closetime: str = None


def create_candle(series):
    df = series.to_frame().T
    return Candle(
        opentime=f"""{df["opentime"]}""",
        open=df["open"],
        high=df["high"],
        low=df["low"],
        close=df["close"],
        volume=df["volume"],
        closetime=f"""{df["closetime"]}"""
    )


@dataclass
class Position:
    symbol: str = None
    opentime_buying_candle: str = None
    buying_timestamp: str = None
    buying_price: float = None
    target_sales_price: float = None
    bet: float = None
    crypto_quantity: float = None


class PreviousPositions:
    """Get previous positions for 1 symbol (crypto)"""

    @dataclass
    class Dataframe:
        opened_positions = pd.DataFrame()
        closed_positions = pd.DataFrame()

    def __init__(self, symbol):
        self.symbol = symbol
        self.df = self.Dataframe()
        self.db_uri = self.load_properties()
        self.get_positions()

    @staticmethod
    def load_properties():
        configs = Properties()
        with open(Path("src/utils/krypto.properties"), "rb") as config_file:
            configs.load(config_file)
            db_uri = configs.get("db_url").data
            return db_uri

    def get_positions(self):
        """This method allows to get the opened position for 1 symbol"""
        # pactole <=> The engine

        for status in ("opened", "closed"):
            pactole = create_engine(self.db_uri, echo=True)
            tb_name = f"{self.symbol}_{status}_positions"

            try:
                positions = pd.read_sql_table(
                    table_name=tb_name,
                    con=pactole
                )
            except ValueError:
                print(f"No {status} positions already existing. A new df will be created")
                positions = pd.DataFrame()

            setattr(self.df, f"{status}_positions", positions)
