import talib


def rsi11(df):
    rsi11 = talib.RSI(df['Close'], 11)
    df['rsi11'] = rsi11
    return df
