import multiprocessing
import pandas as pd
from tqdm import tqdm
import CSV
from Crawling import Stock
from Indicators import Bollinger,IchimokuChart

cnt = ['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21']

def data(cnt):
    realCompanyList = []
    message = f"../subs/filtered_data{cnt}.csv"
    # csv 파일로부터 companyList 가져옴
    companyList = CSV.csvReader(message)
    for company in tqdm(companyList):
        try:
            # company code 가져오기
            code = Stock.get_code(company)
            # stock data 가져오기
            df = Stock.naver_stock(company, code, 20)
            # Bollinger band 상한선
            upper = Bollinger.bollinger(df)[['bb_up']]
            # 일목균형표 후행스팬 25일선
            chikou_span = IchimokuChart.ichimoku(df)[['chikou_span']]
            # 세로 방향으로 이어 붙이기
            merged_df = pd.concat([upper, chikou_span], axis=1, sort=False)
            # 두 지표 값 비교해서 절대값이 0.010 비율 내에 있으면 찾기
            value_df = merged_df[abs((merged_df['bb_up'] - merged_df['chikou_span'])) <= merged_df['bb_up'] * 0.010]
            # 상한선이 후행스팬 값보다 높은 경우만
            value_df = value_df.loc[value_df['bb_up'] >= value_df['chikou_span'], :]

            if value_df['20210511':].empty:
                continue
            else:
                realCompanyList.append(company)

        except AttributeError:
            continue
    CSV.csvAdditer('realCompanyList.csv', realCompanyList)


if __name__ == '__main__':
    p = multiprocessing.Pool(processes=4)
    answer = p.map(data,cnt)
    p.close()