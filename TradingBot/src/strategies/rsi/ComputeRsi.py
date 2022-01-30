import pandas as pd
import numpy as np


class ComputeRsi:
    def __init__(self, df_candles):
        self.df_candles = df_candles
        self.df_candles["close"] = self.df_candles["close"].astype("float", errors="raise")
        self.multiplier = 2 / (1+14)
        self.inv_multiplier = 1 - self.multiplier

    def create_up_and_down_columns(self):
        list_up = []
        list_down = []

        for i, elem in self.df_candles.iterrows():
            if i != 0:
                if self.df_candles["close"][i] > self.df_candles["close"][i-1]:
                    list_up.append(
                        self.df_candles["close"][i] - self.df_candles["close"][i-1]
                    )
                    list_down.append(0)
                else:
                    list_up.append(0)
                    list_down.append(
                        self.df_candles["close"][i-1] - self.df_candles["close"][i]
                    )
            else:
                list_up.append(np.nan)
                list_down.append(np.nan)

        self.df_candles["up"] = list_up
        self.df_candles["down"] = list_down

    def compute_exponential_average(self):
        i = 0
        list_exp_avg_up = []
        list_exp_avg_down = []

        while i < self.df_candles.shape[0]:
            if i > 15:
                list_exp_avg_up.append(
                    (self.df_candles["up"][i] * self.multiplier) + (list_exp_avg_up[i-1] * self.inv_multiplier)
                )
                list_exp_avg_down.append(
                    (self.df_candles["down"][i] * self.multiplier) + (list_exp_avg_down[i-1] * self.inv_multiplier)
                )
                i += 1
            elif i == 15:
                list_exp_avg_up.append(
                    np.mean(self.df_candles["up"][1:15])
                )
                list_exp_avg_down.append(
                    np.mean(self.df_candles["down"][1:15])
                )
                i += 1
            else:
                list_exp_avg_up.append(np.nan)
                list_exp_avg_down.append(np.nan)
                i += 1

        self.df_candles["exp_avg_up"] = list_exp_avg_up
        self.df_candles["exp_avg_down"] = list_exp_avg_down

    def compute_rsi_column(self):
        self.df_candles["rs"] = self.df_candles["exp_avg_up"] / self.df_candles["exp_avg_down"]
        self.df_candles["rsi"] = 100 - (100 / (1 + self.df_candles["rs"]))

    def compute_rsi(self):
        self.create_up_and_down_columns()
        self.compute_exponential_average()
        self.compute_rsi_column()
