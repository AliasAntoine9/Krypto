from dataclasses import dataclass
import pandas as pd


@dataclass
class DataFrame:
    candles = pd.DataFrame()
    candles_tail = pd.DataFrame()
