import talib


def macd(df):
    macd, macdSignal, macdHist = talib.MACD(df['Close'], 12, 26, 9)
    df['macd'] = macd
    df['macdSignal'] = macdSignal

    return df
