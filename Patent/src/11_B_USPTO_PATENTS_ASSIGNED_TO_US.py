__author__ = 'zhuhy'

from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
import re
import time
import random

year = 2018
sum = 0
linecount = 1

f = open('11_B_USPTO_PATENTS_ASSIGNED_TO_US.txt')
user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"
for line in f:
    url = line.replace("2F2015", "2F"+str(year))
    req = Request(url, headers={"User-Agent":user_agent})
    page = urlopen(req)
    soup = BeautifulSoup(page, 'html.parser')

    m = re.search(": (\\d+) patents", soup.text)
    if m is not None:
        print(str(linecount) + " " + str(m.group(1)))
        sum += int(m.group(1))
    linecount += 1
    time.sleep(random.random() * 10)

print(sum)


