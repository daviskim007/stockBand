import pandas as pd
import pandas_datareader as pdr
from datetime import datetime
import mplfinance as mpf
import talib
from bs4 import BeautifulSoup
import requests


stockOfCompany = "삼성전자"
period = None

# 종목 타입에 따라 download url이 다름. 종목 코드 뒤에 .KS .KQ 등이 입력되어야 해서 Download Link 구분 필요
stock_type = {
    'kospi': 'stockMkt',
    'kosdaq': 'kosdaqMkt'
}


# 회사명으로 주식 종목 코드를 획득할 수 있도록 하는 함수
def get_code(df, name):
    code = df.query("name=='{}'".format(name))['code'].to_string(index=False)

    # 위와 같이 code명을 가져오면 앞에 공백이 붙어 있는 상황이 발생하여 앞뒤로 script() 하여 공백 제거
    code = code.strip()
    return code


# download url 조합
def get_download_stock(market_type=None):
    market_type = stock_type[market_type]
    download_link = 'http://kind.krx.co.kr/corpgeneral/corpList.do'
    download_link = download_link + '?method=download'
    download_link = download_link + '&marketType=' + market_type

    df = pd.read_html(download_link, header=0)[0]
    return df


# kospi 종목 코드 목록 다운로드
def get_download_kospi():
    df = get_download_stock('kospi')
    df.종목코드 = df.종목코드.map('{:06d}.KS'.format)
    return df

# kosdaq 종목 코드 목록 다운로드
def get_download_kosdaq():
    df = get_download_stock('kosdaq')
    df.종목코드 = df.종목코드.map('{:06d}.KQ'.format)
    return df

def naver_stock(company,code,pages_to_fetch):
    url = f"http://finance.naver.com/item/sise_day.nhn?code={code}"
    html = BeautifulSoup(requests.get(url,
                                      headers={'User-agent': 'Mozilla/5.0'}).text, "lxml")
    pgrr = html.find("td", class_="pgRR")
    s = str(pgrr.a["href"]).split('=')
    lastpage = s[-1]
    df = pd.DataFrame()
    pages = min(int(lastpage), pages_to_fetch)
    for page in range(1, pages + 1):
        pg_url = '{}&page={}'.format(url, page)
        df = df.append(pd.read_html(requests.get(pg_url,
                                                 headers={'User-agent': 'Mozilla/5.0'}).text)[0])
        tmnow = datetime.now().strftime('%Y-%m-%d %H:%M')
        print('[{}] {} ({}) : {:04d}/{:04d} pages are downloading...'.
              format(tmnow, company, code, page, pages), end="\r")
    df = df.rename(columns={'날짜': 'date', '종가': 'close', '전일비': 'diff'
        , '시가': 'open', '고가': 'high', '저가': 'low', '거래량': 'volume'})
    df['date'] = df['date'].replace('.', '-')
    df = df.dropna()
    df[['close', 'diff', 'open', 'high', 'low', 'volume']] = df[['close',
                                                                 'diff', 'open', 'high', 'low', 'volume']].astype(int)
    df = df[['date', 'open', 'high', 'low', 'close', 'diff', 'volume']]
    return df


# kospi, kosdaq 종목코드 각각 다운로드
kospi_df = get_download_kospi()
kosdaq_df = get_download_kosdaq()

# data frame merge
code_df = pd.concat([kospi_df,kosdaq_df])

# data frame 정리
code_df = code_df[['회사명','종목코드']]

# data frame title 변경 '회사명' = name, 종목코드 = 'code'
code_df = code_df.rename(columns={'회사명':'name','종목코드':'code'})

# 삼성전자의 종목코드 획득, data frame에는 이미 xxxxxx.KX 형태로 조합이 되어있음
code = get_code(code_df,stockOfCompany)


# get_data_yahoo API 를 통해서 yahoo finance의 주식 종목 데이터를 가져온다
df = pdr.get_data_yahoo(code)

# 선택적으로 일정 기간동안의 주식 정보 가져오기
start = datetime(2021, 1, 1)
end = datetime(2021, 5, 21)

df = pdr.get_data_yahoo(code, start, end)
print(df)
# 차트 그리기
colorsetting = mpf.make_marketcolors(up='tab:red',down='tab:blue')
s = mpf.make_mpf_style(marketcolors=colorsetting)
# mpf.plot(df,type='candle',style=s)

# 20일 이동평균선을 구하기
# ma = talib.SMA(df['Close'],20)

# Bollinger band 구하기
upper, middle, lower = talib.BBANDS(df['Close'],20,2)
df['bb_up']= upper
df['bb_mid']=middle
df['bb_low']=lower

#RSI 11 값 추가
rsi11 = talib.RSI(df['Close'],11)
df['rsi11'] = rsi11

#MACD 값 추가
macd, macdSignal, macdHist = talib.MACD(df['Close'],12,26,9)
df['macd'] = macd
df['macdSignal'] = macdSignal

#Stochastic 추가
slowk, slowd = talib.STOCH(df['High'],df['Low'],df['Close'],fastk_period=12,slowk_period=5,slowd_period=5)

#이동평균선
# ma = talib.SMA(df['Close'],period)

#일목균형표
# 전환선
period9_high = df['Close'].rolling(window=9).max() # 과거 9일간 최고가
period9_low = df['Close'].rolling(window=9).min() # 과거 9일간 최저가
tenkan_sen = (period9_high + period9_low) / 2

# 기준선
period26_high = df['Close'].rolling(window=26).max() # 과거 26일간 최고가
period26_low = df['Close'].rolling(window=26).min() # 과거 26일간 최저가
kijun_sen = (period26_high + period26_low) / 2

# 후행스팬
chikou_span = df['Close'].shift(-26) # shift 메서드는 원하는 수만큼 이동시킴
                            # -26 이므로 뒤로(과거) 26만큼 이동시킴
# 선행스팬A
senkou_span_a = ((tenkan_sen + kijun_sen) / 2).shift(26)
# 선행스팬B
period52_high = df['Close'].rolling(window=52).max() # 과거 52일간 최고가
period52_low = df['Close'].rolling(window=52).min() # 과거 52일간 최저가
senkou_span_b = ((period52_high + period52_low) / 2).shift(26)

df['tenkan_sen'] = tenkan_sen
df['kijun_sen'] = kijun_sen
df['chikou_span'] = chikou_span
df['senkou_span_a'] = senkou_span_a
df['senkou_span_b'] = senkou_span_b

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

