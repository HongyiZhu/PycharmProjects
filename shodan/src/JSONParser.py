__author__ = 'hzhu'

import json
import gzip
import mysql.connector


fin = gzip.open("C:\latest.json.gz", 'rb')
for line in fin:
    banner = json.loads(line)
    print banner['ip']
    print banner['asn']
    print banner['data']
    print banner['port']
    print banner['timestamp']
    print banner['hostnames']
    print banner['domains']
    print banner['location']
    print banner['opts']
    print banner['org']
    print banner['isp']
    print banner['os']
    print banner['uptime']
    print banner['link']
    print banner['html']
    print banner['title']
    print banner['product']
    print banner['version']
    print banner['devicetype']
    print banner['info']
    print banner['cpe']