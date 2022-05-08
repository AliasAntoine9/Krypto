import time
import schedule

from src.core.crypto_bot import rsi_strategy


class Scheduler:

    @staticmethod
    def start_schedule():
        symbol = "vet"
        schedule.every(20).seconds.do(
            rsi_strategy,
            symbol=symbol
        )
        while True:
            schedule.run_pending()

    @staticmethod
    def start():
        symbol = "vet"
        while True:
            rsi_strategy(symbol=symbol)
            time.sleep(20)
