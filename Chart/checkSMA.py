import urllib.error
import pandas as pd
import talib

import CSV
from Crawling import Stock
from Indicators import Bollinger,IchimokuChart
from tqdm import tqdm
from time import sleep

pages_to_fetch = 20

if __name__ == '__main__':

    checkSMACompany = []
    message = "filtered/subs/realCompanyList.csv"
    # csv 파일로부터 companyList 가져옴
    companyList = CSV.csvReader(message)
    for company in tqdm(companyList):
        try:
            # company code 가져오기
            code = Stock.get_code(company)
            sleep(0.5)
            # stock data 가져오기
            df = Stock.naver_stock(company, code, pages_to_fetch)
            sleep(0.5)
            # 10일 SMA
            sma10 = talib.SMA(df['Close'],10)[['sma10']]
            # 60일 SMA
            sma60 = talib.SMA(df['Close'],60)
            # 세로 방향으로 이어 붙이기
            merged_df = pd.concat([sma10, sma60], axis=1, sort=False)
            # 컬럼명 변경
            merged_df.columns = ['sma10','sma60']
            # 상한선이 후행스팬 값보다 높은 경우만
            value_df = merged_df.loc[merged_df['sma10'] >= merged_df['sma60'], :]

            if value_df['20210503':].empty:
                continue
            else:
                checkSMACompany.append(company)

        except AttributeError:
            continue
    CSV.csvAdditer('filtered/subs/checkSMACompany.csv',checkSMACompany)
