import pandas as pd

from src.scrapping.rest_api_scrapper import RestApiScrapper
from src.parsing.json_parser import JsonParser
from src.strategies.rsi.compute_rsi import ComputeRsi
from src.core.action import Action


def rsi_strategy(symbol) -> pd.DataFrame:
    # Step 1
    scrapper = RestApiScrapper(symbol=symbol)
    response = scrapper.get_candles()

    # Step 2
    parser = JsonParser()
    candles = parser.transform_to_df(response)

    # Step 3
    Computer = ComputeRsi(candles)
    candles = Computer.compute_rsi()

    # Step 4
    buy_sell_crypto = Action(symbol=symbol, candles=candles)
    buy_sell_crypto.run()

    return candles


if __name__ == "__main__":
    candles_ = rsi_strategy(symbol="vet")
