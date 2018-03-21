import csv

__author__ = "Hongyi Zhu"


class DataPoints:
    def __init__(self, timestamp, x, y, z):
        self.ts = int(timestamp)
        self.x = int(x)
        self.y = int(y)
        self.z = int(z)

data_dict = {}

with open('data.csv') as csvfile:
    reader = csv.reader(csvfile, delimiter=",")
    for row in reader:
        if row[3] in data_dict:
            data_dict[row[3]].append(DataPoints(row[0], row[5], row[6], row[7]))
        else:
            data_dict[row[3]] = []
            data_dict[row[3]].append(DataPoints(row[0], row[5], row[6], row[7]))

for sensor in data_dict:
    print(sensor, len([x for x in data_dict[sensor] if x.ts >= 1478738321000 and x.ts <= 1478741260000]))