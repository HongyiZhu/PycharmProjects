__author__ = 'Hongyi'

import datetime
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import random
import time

search_date = datetime.date(2015, 1, 1)
delta = datetime.timedelta(1)
random.seed()
sum = 0
url_base = "http://worldwide.espacenet.com/searchResults?submitted=true&locale=en_EP&DB=EPODOC&ST=advanced&TI=&AB=&PN=" \
           "&AP=&PR=&PA=&IN=&CPC=&IC=&Submit=Search&PD="
while search_date.year < 2016:
    day = search_date.isoformat().replace("-", "")
    page = urlopen(url_base+day)
    soup = BeautifulSoup(page, 'html.parser')

    m = re.search("(\\d*,\\d+)\sresults found in", soup.text)
    if m is not None:
        print(day + "\t" + str(m.group(1)))
        sum += int(m.group(1).replace(",", ""))
    time.sleep(3 * random.random())
    search_date = search_date + delta

print(sum)
