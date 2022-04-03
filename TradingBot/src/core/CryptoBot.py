from src.scrapping.RestApiScrapper import RestApiScrapper
from src.parsing.JsonParser import JsonParser
from src.strategies.rsi.ComputeRsi import ComputeRsi
from src.core.Action import Action


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
    buy_sell_crypto = Action(symbol=symbol)
    buy_sell_crypto.run(candles=candles)

    return candles


if __name__ == "__main__":
    candles_ = rsi_strategy(symbol="vet")
