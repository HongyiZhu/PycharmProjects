__author__ = 'Hongyi'

from urllib.request import urlopen
from bs4 import BeautifulSoup
import time

country = ["CZ%20GB%20AT%20BE%20BG%20CY%20DK%20EE%20FI%20FR", "DE%20GR%20HU%20IE%20IT%20LV%20LT%20LU%20MT%20NL",
           "PL%20PT%20RO%20SK%20SI%20ES%20SE"]

for year in range(2008, 2015):
    # count = 0
    # for i in range(3):
    url1 = "http://worldwide.espacenet.com/searchResults?" \
          "submitted=true&&DB=EPODOC&ST=advanced&TI=&AB=nano*&PN=&AP=&" \
          "PA=&IN=&CPC=&IC=&Submit=Search&locale=en_EP&PD=" + str(year) + "&PR=JP"
    pg1 = urlopen(url1)
    bs1 = BeautifulSoup(pg1)
    # print(bs1)
    # exit(0)
    time.sleep(5)
    url2 = "http://worldwide.espacenet.com/searchResults?" \
          "submitted=true&&DB=EPODOC&ST=advanced&TI=&AB=nano*&PN=&AP=&" \
          "PA=&IN=&CPC=&IC=&Submit=Search&locale=en_EP&PD=" + str(year) + "&PR=CN"
    pg2 = urlopen(url2)
    bs2 = BeautifulSoup(pg2)
    # print(bs2.find('b').get_text())
    # count += int(bs.find('b').get_text())
    time.sleep(5)
    # print(str(year) + "\t" + str(count))
    print(bs1.find('b').get_text() + "\t" + bs2.find('b').get_text())
