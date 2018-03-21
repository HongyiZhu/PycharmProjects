__author__ = 'Hongyi'

import sqlite3

conn = sqlite3.connect(":memory:")
cur = conn.cursor()

cur.execute("create table temp(lat, lon, p_time, parameter, unit, aqi, category)")

data = [(1, 2, 10, "CO2", "UG/M3", 18, 1),
        (1, 2, 13, "SO2", "UG/M3", 20, 1),
        (1, 2, 15, "CO2", "UG/M3", 15, 1),
        (3, 4, 15, "SO2", "UG/M3", 10, 1)]

cur.executemany("insert into temp(lat, lon, p_time, parameter, unit, aqi, category"
                    ") values ("
                    "?, ?, ?, ?, ?, ?, ?)", data)

for row in cur.execute("select distinct lat, lon from temp where parameter=\"CO2\""):
    print(row)