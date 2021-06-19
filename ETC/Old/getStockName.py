import pandas as pd
import CSV

df = pd.read_html('http://kind.krx.co.kr/corpgeneral/corpList.do?method=download', header=0)[0]
df = df[['회사명']]
companyList = []
for company in df['회사명']:
    companyList.append(company)

CSV.csvWriter('companyL.csv',companyList)

suspendList = CSV.csvReader("../../filtered/suspendedStock.csv")
companyByDeletingSuspended = set(companyList) - set(suspendList)
CSV.csvWriter('companyList.csv', companyByDeletingSuspended)

