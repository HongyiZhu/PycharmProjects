__author__ = 'hzhu'

import MySQLdb as mdb
import xlrd

wb = xlrd.open_workbook(r"C:\Users\hzhu\Desktop\MyLivelyDataSample.xlsx")
table = wb.sheet_by_name(r"MyLivelyData")
mList = []

con = mdb.connect(host="localhost", user="zhuhy", passwd="Edwardsj211211", db="mylively")

with con:
    cur = con.cursor()

    for i in range(0, table.nrows % 1000):
        print i
        for j in range(1, 1001):
            if 1000 * i + j >= table.nrows:
                break
            row = table.row_values(i * 1000 + j)
            hubBID = row[0]
            hubID = row[1]
            userID = int(row[2])
            timeZone = row[3]
            sensorBID = row[4]
            category = row[5]
            f_force = int(row[7])
            unixTimeStamp = str(int(row[8]))
            mList.append((hubBID, hubID, userID, timeZone, sensorBID, category, f_force, unixTimeStamp))

        cur.executemany(
            """insert into livelydata (HubBluetoothID, HubID, UserID, TimeZone,
            SensorBluetoothID, SensorCategory, F_Force, UnixTime)
            values (%s, %s, %s, %s, %s, %s, %s, %s)""",
            mList)
        mList = []






