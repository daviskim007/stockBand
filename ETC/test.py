import csv
import numpy as np

read_list = []
f = open('companyList01.csv', 'r')
rdr = csv.reader(f)
for line in rdr:
    read_list.append(line)
    print(line)
print(read_list[3])
f.close()
