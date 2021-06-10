import mplfinance as mpf
import pandas as pd

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
    # Bollinger band 상한선
    upper = Bollinger.bollinger(df)[['bb_up']]
    # 일목균형표 후행스팬 25일선
    chikou_span = IchimokuChart.ichimoku(df)[['chikou_span']]
    # 세로 방향으로 이어 붙이기
    merged_df = pd.concat([upper, chikou_span], axis=1, sort=False)
    print(merged_df)

