import pandas as pd
import CSV

df = pd.read_html('http://kind.krx.co.kr/corpgeneral/corpList.do?method=download', header=0)[0]
df = df[['회사명']]
companyList = []
for company in df['회사명']:
    companyList.append(company)

suspendList = CSV.csvReader("suspendedStock.csv")
companyByDeletingSuspended = set(companyList) - set(suspendList)
companyByDeletingSuspended = list(companyByDeletingSuspended)
cnt = 1
for splicied in range(0, len(companyByDeletingSuspended), 100):
    message = f"subs/filtered_data{cnt}.csv"
    CSV.csvWriter(message,companyByDeletingSuspended[splicied:splicied + 100])
    cnt+=1
