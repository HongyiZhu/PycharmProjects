__author__ = 'hzhu'
import os
import csv
import random
import string

def calc(test):
    prior_num = []
    firstUSCount = 0
    inventorUSCount = 0
    companyUSCount = 0
    nonOverLap = 0
    for patent in test:
        inventor = patent[3]
        company = patent[4]
        pn = patent[9]
        if company.find('[US]') != -1:
            companyUSCount += 1
        if inventor.find('[US]') != -1:
            inventorUSCount += 1
            if inventor.find('[') == inventor.find('[US]'):
                firstUSCount += 1
        pnlist = string.split(pn, ';')
        for i in range(len(pnlist)):
            pnlist[i] = pnlist[i].strip()
        flag = True
        for pnumber in pnlist:
            if pnumber in prior_num:
                flag = False
            else:
                prior_num.append(pnumber)
        if flag:
            nonOverLap += 1
    print('Size:\t\t\t\t' + str(len(test)))
    print('Non-Overlap:\t\t' + str(nonOverLap))
    print('firstInventorUS:\t' + str(firstUSCount))
    print('existInventorUS:\t' + str(inventorUSCount))
    print('companyUS:\t\t\t' + str(companyUSCount))
    # print len(prior_num)-len(set(prior_num))
    print

folder = 'C:/PR/'
filenameList = os.listdir(folder)
sampleCount = 0
header = []
sample = []
for filename in filenameList:
    with open(folder+filename, 'rb') as f:
        reader = csv.reader(f)
        header = reader.next()
        for row in reader:
            # print row[9].strip()
            sample += [row]
            sampleCount += 1
# random.shuffle(sample)
# print sampleCount
set1 = sample[:sampleCount / 3]
set2 = sample[sampleCount / 3: sampleCount / 3 * 2]
set3 = sample[sampleCount / 3 * 2:]
calc(sample)
calc(set1)
calc(set2)
calc(set3)

