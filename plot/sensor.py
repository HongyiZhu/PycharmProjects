__author__ = 'Hongyi'

from numpy import *
import csv
import matplotlib
import matplotlib.pyplot as plt

# Global plot
f = plt.figure(1)
plt.subplot(111)
timebase = 1440469800


def plotChair(upper, lower=0):
    chair = open("D:/sensors/E555.csv")
    E555 = csv.DictReader(chair)
    for line in E555:
        if line['event_id'] != '1':
            time = float(line['event_timestamp']) - timebase
            if lower < time < upper:
                plt.scatter(time, 1, color="r", s=1, label="E555")
    chair.close()


def plotBath(upper, lower=0):
    bath = open("D:/sensors/E755.csv")
    E755 = csv.DictReader(bath)
    for line in E755:
        if line['event_id'] != '1':
            time = float(line['event_timestamp']) - timebase
            if lower < time < upper:
                plt.scatter(time, 0.4, color="g", s=1, label="E755")
    bath.close()


def plotDown(upper, lower=0):
    down = open("D:/sensors/E74C.csv")
    E74C = csv.DictReader(down)
    for line in E74C:
        if line['event_id'] != '1':
            time = float(line['event_timestamp']) - timebase
            if lower < time < upper:
                plt.scatter(time, 0.6, color="b", s=1, label="E74C")
    down.close()


def plotUp(upper, lower=0):
    up = open("D:/sensors/E93D.csv")
    E93D = csv.DictReader(up)
    for line in E93D:
        if line['event_id'] != '1':
            time = float(line['event_timestamp']) - timebase
            if lower < time < upper:
                plt.scatter(time, 0.8, color="m", s=1, label="E93D")
    up.close()


def plotHuman(upper, lower=0):
    human = open("D:/sensors/EB99.csv")
    EB99 = csv.DictReader(human)
    for line in EB99:
        if line['event_id'] != '1':
            time = float(line['event_timestamp']) - timebase
            if lower < time < upper:
                plt.scatter(time, 1.2, color="y", s=1, label="EB99")
    human.close()


def plotting(upper, lower=0):
    # plotBath(upper, lower)
    # plotChair(upper, lower)
    plotUp(upper, lower)
    plotDown(upper, lower)
    plotHuman(upper, lower)

plotting(1040, 1035)
plt.xlabel("seconds")
plt.show()
# for line in E555:
#     print(line)
