import talib


def bollinger(df):
    # Bollinger band 구하기
    upper, middle, lower = talib.BBANDS(df['Close'], 20, 2)
    df['bb_up'] = upper
    df['bb_mid'] = middle
    df['bb_low'] = lower

    return df
