
import pandas as pd
import CSV
from Crawling import Stock
from Indicators import Bollinger,IchimokuChart

pages_to_fetch = 20

if __name__ == '__main__':
    realCompanyList = []
    # csv 파일로부터 companyList 가져옴
    companyList = CSV.csvReader('companyList.csv')

    for company in companyList:
        try:
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
            # 두 지표 값 비교해서 절대값이 500 아래이면 찾기
            value_df = merged_df[abs((merged_df['bb_up'] - merged_df['chikou_span'])) <= 500]
            if value_df['20210415':].empty:
                continue
            else:
                realCompanyList.append(company)

        except AttributeError:
            continue

    print(realCompanyList)
