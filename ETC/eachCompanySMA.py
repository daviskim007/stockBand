import mplfinance as mpf
import pandas as pd
import talib

import CSV
from Crawling import Stock
from Indicators import Bollinger,IchimokuChart
from CSV import csvReader

pd.set_option('display.max_row', 500)
pd.set_option('display.max_columns', 100)

company = "인터지스"
pages_to_fetch = 20

if __name__ == '__main__':

    # company code 가져오기
    code = Stock.get_code(company)
    # stock data 가져오기
    df = Stock.naver_stock(company, code, pages_to_fetch)
    # 10일선
    sma10 = talib.SMA(df['Close'],10)
    # 60일선
    sma60 = talib.SMA(df['Close'],60)
    # 세로 방향으로 이어 붙이기
    merged_df = pd.concat([sma10, sma60], axis=1, sort=False)
    # 컬럼명 변경
    merged_df.columns = ['sma10','sma60']
    specificData = merged_df.loc['20210603']
    value_df = specificData.loc[specificData['sma10'] >= specificData['sma60']]
    value_df
    # if value_df.empty:
    #     print('false')
    # else:
    #     print("true")

