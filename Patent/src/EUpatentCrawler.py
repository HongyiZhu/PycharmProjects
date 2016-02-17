__author__ = 'Hongyi'

from urllib.request import urlopen
from bs4 import BeautifulSoup
import time

country = ["CZ%20GB%20AT%20BE%20BG%20CY%20DK%20EE%20FI%20FR", "DE%20GR%20HU%20IE%20IT%20LV%20LT%20LU%20MT%20NL",
           "PL%20PT%20RO%20SK%20SI%20ES%20SE"]

for year in range(1999, 2000):
    # deal with other 3 countries/total
    url1 = "http://worldwide.espacenet.com/searchResults?" \
        "submitted=true&&DB=EPODOC&ST=advanced&TI=&AB=nano*&PN=&AP=&" \
        "PA=&IN=&CPC=&IC=&Submit=Search&locale=en_EP&PD=" + str(year) + "&PR=US"
    pg1 = urlopen(url1)
    bs1 = BeautifulSoup(pg1)
    time.sleep(5)
    print(bs1.find('b').get_text())

    # deal with EU27
    # count = 0
    # for i in range(3):
    #     url = "http://worldwide.espacenet.com/searchResults?" \
    #         "submitted=true&&DB=EPODOC&ST=advanced&TI=&AB=nano*&PN=&AP=&" \
    #         "PA=&IN=&CPC=&IC=&Submit=Search&locale=en_EP&PD=" + str(year) + "&PR=" + country[i]
    #     pg = urlopen(url)
    #     bs = BeautifulSoup(pg)
    #     count += int(bs.find('b').get_text())
    #     time.sleep(5)
    # print(count)
