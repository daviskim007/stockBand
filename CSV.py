# -*- coding: utf-8 -*-
import csv
import numpy as np


# Function for reading .csv file
def csvReader(filename):
    item_list = []
    with open(filename, encoding='UTF8') as file:
        reader = csv.reader(file)
        for item in reader:
            item_list.append(item)
    company_list = np.concatenate(item_list).tolist()
    return company_list


def csvWriter(filename, data):
    with open(filename, 'w', newline='', encoding='UTF8') as file:
        writer = csv.writer(file)
        writer.writerow(data)

    return writer

def csvAdditer(filename, data):
    with open(filename, 'a', newline='', encoding='UTF8') as file:
        writer = csv.writer(file)
        writer.writerow(data)

    return writer


# # 반복문해서 csv 로 지정 갯수 만큼 저장
# filtered_data = csvReader('filtered/filtered_data.csv')
# cnt = 1
# for splicied in range(0, len(filtered_data), 50):
#     message = f"filtered/subs/filtered_data{cnt}.csv"
#     csvWriter(message,filtered_data[splicied:splicied +50])
#     cnt+=1
