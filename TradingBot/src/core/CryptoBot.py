from TradingBot.src.strategies.rsi.ParseMarketData import ParseMarketData
from TradingBot.src.strategies.rsi.ComputeRsi import ComputeRsi
from TradingBot.src.core.Position import Position


def rsi_strategy(symbol):
    # Step 1
    Parser = ParseMarketData(symbol=symbol)
    df_candles = Parser.create_dataframe()

    # Step 2
    Computer = ComputeRsi(df_candles=df_candles)
    Computer.compute_rsi()

    # Step 3
    position = Position(symbol, )
    position.run(df_candles=df_candles)

    # step 4
    # records_buy_sell_movements_in_database()

    return df_candles


if __name__ == "__main__":
    df_candles_ = rsi_strategy(symbol="vet")
