from src.strategies.rsi.ParseMarketData import ParseMarketData
from src.strategies.rsi.ComputeRsi import ComputeRsi
from src.core.Position import create_new_position


def rsi_strategy(symbol, all_positions):
    # Step 1
    Parser = ParseMarketData(symbol=symbol)
    df_close = Parser.create_dataframe()

    # Step 2
    Computer = ComputeRsi(df_close=df_close)
    Computer.compute_rsi()

    # Step 3
    create_new_position(symbol=symbol, all_positions=all_positions, df_close=df_close)

    return df_close


if __name__ == "__main__":
    df_close_ = rsi_strategy(symbol="VET", all_positions=[])
