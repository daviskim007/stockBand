def ichimoku(df):
    # 전환선
    period9_high = df['Close'].rolling(window=9).max()  # 과거 9일간 최고가
    period9_low = df['Close'].rolling(window=9).min()  # 과거 9일간 최저가
    tenkan_sen = (period9_high + period9_low) / 2

    # 기준선
    period26_high = df['Close'].rolling(window=25).max()  # 과거 26일간 최고가
    period26_low = df['Close'].rolling(window=25).min()  # 과거 26일간 최저가
    kijun_sen = (period26_high + period26_low) / 2

    # 후행스팬
    chikou_span = df['Close'].shift(-25)  # shift 메서드는 원하는 수만큼 이동시킴
    # -26 이므로 뒤로(과거) 26만큼 이동시킴
    # 선행스팬A
    senkou_span_a = ((tenkan_sen + kijun_sen) / 2).shift(25)
    # 선행스팬B
    period52_high = df['Close'].rolling(window=50).max()  # 과거 52일간 최고가
    period52_low = df['Close'].rolling(window=50).min()  # 과거 52일간 최저가
    senkou_span_b = ((period52_high + period52_low) / 2).shift(25)

    df['tenkan_sen'] = tenkan_sen
    df['kijun_sen'] = kijun_sen
    df['chikou_span'] = chikou_span
    df['senkou_span_a'] = senkou_span_a
    df['senkou_span_b'] = senkou_span_b

    return df