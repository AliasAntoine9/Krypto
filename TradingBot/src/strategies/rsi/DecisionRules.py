from datetime import timedelta


def get_last_rsi_value_inf_to_30(df):
    trigger_moment = None
    for i, row in df.iterrows():
        if row["rsi"] < 30:
            trigger_moment = i
    return trigger_moment


def create_column_rsi_above_35(df):
    df["rsi_above_35"] = df["rsi"].apply(lambda x: True if x >= 35 else False)


def count_values_above_35(candles_tail):
    last_row = candles_tail.shape[0]
    if candles_tail["rsi", last_row] > 30:
        nb_of_values_above_35 = candles_tail["rsi_above_35"].value_counts()[1]
        return nb_of_values_above_35
    else:
        return 0


def check_which_candles_are_above_35_rsi(nb_of_values_above_35, candles_tail):
    """
    opentime_trigger_candle -> It's the opentime which trigger the buying signal.
    So it's the previous opentime before the opentime of the candle to buy.
    """
    c = 0
    if nb_of_values_above_35 >= 5:
        for i, row in candles_tail.iterrows():
            if row["rsi_above_35"]:
                c += 1
            if c == 5:
                opentime_candle_to_buy = row["closetime"] + timedelta(seconds=1)
                opentime_trigger_candle = row["opentime"]
                return opentime_candle_to_buy, opentime_trigger_candle, candles_tail
        return "", "", candles_tail
    else:
        return "", "", candles_tail


def search_candle_to_buy(df):
    create_column_rsi_above_35(df)

    last_row = df.shape[0]
    signal = get_last_rsi_value_inf_to_30(df)
    candles_tail = df[signal:last_row]

    nb_of_values_above_35 = count_values_above_35(candles_tail)
    opentime_candle_to_buy, opentime_trigger_candle, candles_tail = check_which_candles_are_above_35_rsi(
        nb_of_values_above_35,
        candles_tail
    )

    candle_trigger = candles_tail[last_row - 1]
    candle_to_buy = candles_tail[last_row]

    return candle_to_buy, candle_trigger, candles_tail
