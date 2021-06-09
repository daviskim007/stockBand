import CSV


filtered_data = CSV.csvReader('companyBydeletingSuspended.csv')
cnt = 1
for splicied in range(0, len(filtered_data), 100):
    message = f"subs/filtered_data{cnt}.csv"
    CSV.csvWriter(message,filtered_data[splicied:splicied + 100])
    cnt+=1
