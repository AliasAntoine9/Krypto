import time

import schedule

from TradingBot.src.core.CryptoBot import rsi_strategy


class Scheduler:

    @staticmethod
    def start_schedule():
        symbol = "vet"
        all_positions = get_previous_positions_for(symbol=symbol)
        schedule.every(20).seconds.do(
            rsi_strategy,
            symbol=symbol,
            all_positions=all_positions
        )
        while True:
            schedule.run_pending()

    @staticmethod
    def start():
        symbol = "vet"
        all_positions = get_previous_positions_for(symbol=symbol)
        while True:
            rsi_strategy(symbol=symbol, all_positions=all_positions)
            time.sleep(20)
