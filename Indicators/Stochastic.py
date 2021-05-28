import talib


def stochastic(df):
    slowk, slowd = talib.STOCH(df['High'], df['Low'], df['Close'], fastk_period=12, slowk_period=5, slowd_period=5)
    df['slowk'] = slowk
    df['slowd'] = slowd
    return df
