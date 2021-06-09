import time

import pandas as pd
from datetime import datetime
from bs4 import BeautifulSoup
import requests

stockOfCompany = "삼성전자"
period = None
realCompany = []
cnt = 0
pages_to_fetch = 10
# 종목 타입에 따라 download url이 다름. 종목 코드 뒤에 .KS .KQ 등이 입력되어야 해서 Download Link 구분 필요
stock_type = {
    'kospi': 'stockMkt',
    'kosdaq': 'kosdaqMkt'
}

# kospi 종목 코드 목록 다운로드
def get_download_kospi():
    df = get_download_stock('kospi')
    df.종목코드 = df.종목코드.map('{:06d}'.format)
    return df


# kosdaq 종목 코드 목록 다운로드
def get_download_kosdaq():
    df = get_download_stock('kosdaq')
    df.종목코드 = df.종목코드.map('{:06d}'.format)
    return df

# 회사명으로 주식 종목 코드를 획득할 수 있도록 하는 함수
def get_code(name):
    kospi_df = get_download_kospi()
    kosdaq_df = get_download_kosdaq()

    # data frame merge
    '''index=number, columns = 회사명, 종목코드, 홈페이지, 지역'''
    code_df = pd.concat([kospi_df, kosdaq_df])

    # data frame 정리
    '''index=number, columns = 회사명, 종목코드'''
    code_df = code_df[['회사명', '종목코드']]

    # data frame title 변경 '회사명' = name, 종목코드 = 'code'
    '''index=number, columns = name, code'''
    code_df = code_df.rename(columns={'회사명': 'name', '종목코드': 'code'})

    code = code_df.query("name=='{}'".format(name))['code'].to_string(index=False)

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



def naver_stock(company,code,pages_to_fetch):
    url = f"http://finance.naver.com/item/sise_day.nhn?code={code}"
    html = BeautifulSoup(requests.get(url,
                                      headers={'User-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                                                             "AppleWebKit/537.36 (KHTML, like Gecko) "
                                                             "Chrome/90.0.4430.212 "
                                                             "Safari/537.36"}).text, "lxml")
    pgrr = html.find("td", class_="pgRR")
    s = str(pgrr.a["href"]).split('=')
    lastpage = s[-1]
    df = pd.DataFrame()
    pages = min(int(lastpage), pages_to_fetch)
    for page in range(1, pages + 1):
        pg_url = '{}&page={}'.format(url, page)
        df = df.append(pd.read_html(requests.get(pg_url,
                                                 headers={'User-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                                                                        "AppleWebKit/537.36 (KHTML, like Gecko) "
                                                                        "Chrome/90.0.4430.212 Safari/537.36"}).text)[0])
        tmnow = datetime.now().strftime('%Y-%m-%d %H:%M')
        print('[{}] {} ({}) : {:04d}/{:04d} pages are downloading...'.
              format(tmnow, company, code, page, pages), end="\r")
    df = df.rename(columns={'날짜': 'Date', '종가': 'Close', '전일비': 'Diff'
        , '시가': 'Open', '고가': 'High', '저가': 'Low', '거래량': 'Volume'})
    df['Date'] = df['Date'].replace('.', '-')
    df = df.dropna()
    df[['Close', 'Diff', 'Open', 'High', 'Low', 'Volume']] = df[['Close',
                                                                 'Diff', 'Open', 'High', 'Low', 'Volume']].astype(int)
    df = df[['Date', 'Open', 'High', 'Low', 'Close', 'Diff', 'Volume']]
    df.index = pd.DatetimeIndex(df['Date'])
    df = df.sort_index(ascending=True)
    df = df[['Open', 'High', 'Low', 'Close', 'Diff', 'Volume']]
    return df
