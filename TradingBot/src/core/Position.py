import pickle
from os.path import exists
from pathlib import Path
from src.strategies.rsi.DecisionRules import search_candle_to_buy
from datetime import datetime


class Position:

    def __init__(self, symbol, candle_trigger, candle_to_buy):
        self.symbol = symbol
        self.candle_trigger = candle_trigger
        self.candle_to_buy = candle_to_buy
        self.real_buy_moment = ""
        self.bet = 0
        self.crypto_quantity = 0
        self.buying_value = 0

    def buy(self):
        pass


def load_previous_positions():
    if not exists(Path("database/all_positions")):
        return []
    else:
        try:
            with open(Path("database/all_positions"), "rb") as handle:
                all_positions = pickle.load(handle)
        except EOFError:
            return []
        return all_positions


def get_previous_positions_for(symbol):
    all_positions = load_previous_positions()
    all_positions_symbol = []
    for position in all_positions:
        if position.symbol == symbol:
            all_positions_symbol.append(position)
    return all_positions_symbol


def create_list_all_candles_bought(all_positions):
    all_candles_bought = []
    for position in all_positions:
        all_candles_bought.append(position.candle_to_buy)
    return all_candles_bought


def candle_to_buy_is_the_last_candle(df_tail, candle_trigger):
    last_row = df_tail.last_valid_index()
    if df_tail["closeTime"][last_row] == candle_trigger:
        return True
    else:
        return False


def create_new_position(symbol, all_positions, df_close):
    candle_to_buy, candle_trigger, df_tail = search_candle_to_buy(df=df_close)
    all_candles_bought = create_list_all_candles_bought(all_positions)

    if candle_to_buy not in all_candles_bought and candle_to_buy_is_the_last_candle(df_tail, candle_trigger):
        NewPosition = Position(symbol=symbol, candle_trigger=candle_trigger, candle_to_buy=candle_to_buy)
        all_positions.append(NewPosition)
        print(f"""Time: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}  |  New position created""")
    else:
        print(f"""Time: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}  |  I didn't bought anything...""")
