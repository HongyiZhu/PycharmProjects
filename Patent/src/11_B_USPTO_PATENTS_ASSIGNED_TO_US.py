__author__ = 'zhuhy'

from bs4 import BeautifulSoup
from urllib.request import urlopen
import re

year = 2015
sum = 0
linecount = 1

f = open('11_B_USPTO_PATENTS_ASSIGNED_TO_US.txt')
for line in f:
    url = line.replace("2F2015", "2F"+str(year))
    page = urlopen(url)
    soup = BeautifulSoup(page, 'html.parser')

    m = re.search(": (\\d+) patents", soup.text)
    if m is not None:
        print(str(linecount) + " " + str(m.group(1)))
        sum += int(m.group(1))
    linecount += 1

print(sum)


