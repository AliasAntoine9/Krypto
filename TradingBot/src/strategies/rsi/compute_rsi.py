import numpy as np
import pandas as pd


class ComputeRsi:
    def __init__(self, candles):
        self.candles = candles
        self.multiplier = 2 / (1+14)
        self.inv_multiplier = 1 - self.multiplier

    def compute_rsi(self) -> pd.DataFrame:
        """Main method of ComputerRsi object"""
        self.create_close_columns()
        self.create_up_and_down_columns()
        self.create_exponential_average()
        self.create_rs_and_rsi()
        return self.candles

    def create_close_columns(self) -> None:
        """
        This method is changing the type of 'close' column and adding 'close_lag' column
        close_lag has same values than close column, but the values are lagged with 1 period
        """
        self.candles["close"] = self.candles["close"].astype("float", errors="raise")
        self.candles["close_lag"] = self.candles["close"].shift(1)

    def create_up_and_down_columns(self) -> None:
        """Create up and down columns which will be used to compute exponential average column"""
        # Unload self
        candles = self.candles.copy()

        # Remove first line
        candles = candles.loc[1:]

        # Create a mask which keep only up moves
        mask = candles["close"] > candles["close_lag"]

        # Add up column
        candles.loc[mask, "up"] = candles["close"] - candles["close_lag"]
        candles.loc[~mask, "up"] = 0.0

        # Add down column
        candles.loc[~mask, "down"] = candles["close_lag"] - candles["close"]
        candles.loc[mask, "down"] = 0.0

        # Load self
        self.candles = candles

    def create_exponential_average(self) -> None:
        """
        This method is adding 2 columns to candles df: exp_avg_up and exp_avg_down
        These columns will be used to compute rs (Relative Strength) column
        """
        i = 0
        list_exp_avg_up = []
        list_exp_avg_down = []

        while i < self.candles.shape[0]:
            if i > 15:
                list_exp_avg_up.append(
                    (self.candles["up"][i] * self.multiplier) + (list_exp_avg_up[i-1] * self.inv_multiplier)
                )
                list_exp_avg_down.append(
                    (self.candles["down"][i] * self.multiplier) + (list_exp_avg_down[i-1] * self.inv_multiplier)
                )
                i += 1
            elif i == 15:
                list_exp_avg_up.append(
                    np.mean(self.candles["up"][:15])
                )
                list_exp_avg_down.append(
                    np.mean(self.candles["down"][:15])
                )
                i += 1
            else:
                list_exp_avg_up.append(np.nan)
                list_exp_avg_down.append(np.nan)
                i += 1

        self.candles["exp_avg_up"] = list_exp_avg_up
        self.candles["exp_avg_down"] = list_exp_avg_down

    def create_rs_and_rsi(self) -> None:
        """
        This method is adding 2 columns to candles df: rs (Relative Strength) and rsi (Relative Strength Index)
        """
        self.candles["rs"] = self.candles["exp_avg_up"] / self.candles["exp_avg_down"]
        self.candles["rsi"] = 100 - (100 / (1 + self.candles["rs"]))
