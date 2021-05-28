import csv
import numpy as np

#Function for reading .csv file
def csvReader(filename):
    item_list = []
    with open(filename) as file:
        reader = csv.reader(file)
        for item in reader:
            item_list.append(item)
    company_list = np.concatenate(item_list).tolist()
    return company_list

def csvWriter(filename):
    with open(filename,'w',newline='') as file:
        writer = csv.writer(file)

    return writer
