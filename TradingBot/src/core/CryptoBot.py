from TradingBot.src.scrapping.RestApiScrapper import RestApiScrapper
from TradingBot.src.parsing.JsonParser import JsonParser
from TradingBot.src.strategies.rsi.ComputeRsi import ComputeRsi
from TradingBot.src.core.Position import Position


def rsi_strategy(symbol):
    # Step 1
    scrapper = RestApiScrapper(symbol=symbol)
    response = scrapper.get_candles()

    # Step 2
    parser = JsonParser()
    candles = parser.transform_to_df(response)

    # Step 3
    Computer = ComputeRsi(candles)
    Computer.compute_rsi()

    # Step 4
    position = Position(symbol)
    position.run(candles=candles)

    # step 5
    # records_buy_sell_movements_in_database()

    return candles


if __name__ == "__main__":
    candles_ = rsi_strategy(symbol="vet")
