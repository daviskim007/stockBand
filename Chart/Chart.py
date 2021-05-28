import mplfinance as mpf

# 차트 그리기
colorsetting = mpf.make_marketcolors(up='tab:red',down='tab:blue')
s = mpf.make_mpf_style(marketcolors=colorsetting)
# mpf.plot(df,type='candle',style=s)

#기존 차트 추가
# macd 추가 버전
# apds = [mpf.make_addplot(df[['bb_up','bb_mid','bb_low']])]
# rsi , macd 추가 버전
# apds = [mpf.make_addplot(df[['bb_up','bb_mid','bb_low']]),mpf.make_addplot((df['rsi11']),panel=1,color='g'),mpf.make_addplot((df[['macd','macdSignal']]),panel=2)]
# 일목균형표 추가버전
apds = [mpf.make_addplot(df[['tenkan_sen','kijun_sen','chikou_span','senkou_span_a','senkou_span_b']])]


if __name__ == '__main__':
    # print(chikou_span)
    # 기본 버전
    # mpf.plot(df, type='candle',style=s)

    # macd 추가 버전
    # mpf.plot(df, type='candle',addplot=apds,style=s)

    # 기존차트 추가 버전
    # mpf.plot(df,type='candle',addplot=apds,style=s,fill_between=dict(y1=df['bb_up'].values,y2=df['bb_low'].values,alpha=0.5,color='grey'),mav=20)

    # 일목균형표 추가버전
    mpf.plot(df, type='candle',addplot=apds,style=s)