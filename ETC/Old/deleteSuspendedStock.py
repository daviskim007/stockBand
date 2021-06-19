import CSV

companyList = CSV.csvReader("companyList.csv")
suspendList = CSV.csvReader("../../filtered/suspendedStock.csv")

companyByDeletingSuspended = set(companyList) - set(suspendList)
print(companyByDeletingSuspended)
CSV.csvWriter('companyBydeletingSuspended.csv', companyByDeletingSuspended)