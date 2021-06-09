import CSV


companyList = CSV.csvReader("companyList.csv")
suspendList = CSV.csvReader("suspendedStock.csv")

companyByDeletingSuspended = set(companyList) - set(suspendList)
CSV.csvWriter('companyBydeletingSuspended.csv',companyByDeletingSuspended)