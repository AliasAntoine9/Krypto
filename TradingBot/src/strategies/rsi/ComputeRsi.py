import pandas as pd
import numpy as np


class ComputeRsi:
    def __init__(self, df_close):
        self.df_close = df_close
        self.df_close["close"] = self.df_close["close"].astype("float", errors="raise")
        self.multiplier = 2 / (1+14)
        self.inv_multiplier = 1 - self.multiplier

    def create_up_and_down_columns(self):
        list_up = []
        list_down = []

        for i, elem in self.df_close.iterrows():
            if i != 0:
                if self.df_close["close"][i] > self.df_close["close"][i-1]:
                    list_up.append(
                        self.df_close["close"][i] - self.df_close["close"][i-1]
                    )
                    list_down.append(0)
                else:
                    list_up.append(0)
                    list_down.append(
                        self.df_close["close"][i-1] - self.df_close["close"][i]
                    )
            else:
                list_up.append(np.nan)
                list_down.append(np.nan)

        self.df_close["up"] = list_up
        self.df_close["down"] = list_down

    def compute_exponential_average(self):
        i = 0
        list_exp_avg_up = []
        list_exp_avg_down = []

        while i < self.df_close.shape[0]:
            if i > 15:
                list_exp_avg_up.append(
                    (self.df_close["up"][i] * self.multiplier) + (list_exp_avg_up[i-1] * self.inv_multiplier)
                )
                list_exp_avg_down.append(
                    (self.df_close["down"][i] * self.multiplier) + (list_exp_avg_down[i-1] * self.inv_multiplier)
                )
                i += 1
            elif i == 15:
                list_exp_avg_up.append(
                    np.mean(self.df_close["up"][1:15])
                )
                list_exp_avg_down.append(
                    np.mean(self.df_close["down"][1:15])
                )
                i += 1
            else:
                list_exp_avg_up.append(np.nan)
                list_exp_avg_down.append(np.nan)
                i += 1

        self.df_close["exp_avg_up"] = list_exp_avg_up
        self.df_close["exp_avg_down"] = list_exp_avg_down

    def compute_rsi_column(self):
        self.df_close["rs"] = self.df_close["exp_avg_up"] / self.df_close["exp_avg_down"]
        self.df_close["rsi"] = 100 - (100 / (1 + self.df_close["rs"]))

    def compute_rsi(self):
        self.create_up_and_down_columns()
        self.compute_exponential_average()
        self.compute_rsi_column()
