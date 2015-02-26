__author__ = 'hzhu'

import mysql.connector

cnx = mysql.connector.connect(user='zhuhy', password='Sh0d@n7e', host='128.196.27.147', database='shodan')
cursor = cnx.cursor()

query = ("Select count(*) from scadashodan")
cursor.execute(query)

for (count,) in cursor:
    print count

cnx.close()