import schedule
from TradingBot.src.core.CryptoBot import rsi_strategy
from TradingBot.src.core.Position import Position, get_previous_positions_for


class Scheduler:

    @staticmethod
    def start():
        symbol = "VET"
        all_positions = get_previous_positions_for(symbol=symbol)
        schedule.every(20).seconds.do(
            rsi_strategy,
            symbol=symbol,
            all_positions=all_positions
        )
        while True:
            schedule.run_pending()
