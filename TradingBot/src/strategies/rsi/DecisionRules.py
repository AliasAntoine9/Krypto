from datetime import timedelta


def get_last_rsi_value_inf_to_30(df):
    trigger_moment = None
    for i, row in df.iterrows():
        if row["rsi"] < 30:
            trigger_moment = i
    return trigger_moment


def create_column_rsi_above_35(df):
    df["rsi_above_35"] = df["rsi"].apply(lambda x: True if x >= 35 else False)


def count_values_above_35(df_tail):
    last_row = df_tail.last_valid_index()
    if df_tail["rsi"][last_row] > 30:
        nb_of_values_above_35 = df_tail["rsi_above_35"].value_counts()[1]
        return nb_of_values_above_35
    else:
        return 0


def check_which_candles_are_above_35_rsi(nb_of_values_above_35, df_tail):
    c = 0
    if nb_of_values_above_35 >= 5:
        for i, row in df_tail.iterrows():
            if row["rsi_above_35"]:
                c += 1
            if c == 5:
                opentime_candle_to_buy = row["closetime"] + timedelta(seconds=1)
                opentime_candle_trigger = row["opentime"]
                return opentime_candle_to_buy, opentime_candle_trigger, df_tail
        return "", "", df_tail
    else:
        return "", "", df_tail


def search_candle_to_buy(df):
    create_column_rsi_above_35(df)

    last_row = df.shape[0]
    signal = get_last_rsi_value_inf_to_30(df)
    df_tail = df[signal:last_row]

    nb_of_values_above_35 = count_values_above_35(df_tail)
    opentime_candle_to_buy, opentime_candle_trigger, df_tail = check_which_candles_are_above_35_rsi(
        nb_of_values_above_35,
        df_tail
    )

    return opentime_candle_to_buy, opentime_candle_trigger, df_tail
