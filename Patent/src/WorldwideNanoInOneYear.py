__author__ = 'Hongyi'

import datetime
from selenium import webdriver
from bs4 import BeautifulSoup
import re
import random
import time


search_date = datetime.date(2016, 1, 1)
delta = datetime.timedelta(1)
random.seed()
sum = 0
search_page = "https://worldwide.espacenet.com/advancedSearch?locale=en_EP"
url_base = "https://worldwide.espacenet.com/searchResults?submitted=true&locale=en_EP&DB=EPODOC&ST=advanced&TI=&AB=&PN=" \
           "&AP=&PR=&PA=&IN=&CPC=&IC=&Submit=Search&PD="
cookie = "LevelXLastSelectedDataSource=EPODOC; JSESSIONID=v1p20iZiazrqRkvqkUVTKrkI.espacenet_levelx_prod_1; menuCurrentSearch=%2F%2Fworldwide.espacenet.com%2FsearchResults%3FAB%3D%26AP%3D%26CPC%3D%26DB%3DEPODOC%26IC%3D%26IN%3D%26PA%3D%26PD%3D20160101%26PN%3D%26PR%3D%26ST%3Dadvanced%26Submit%3DSearch%26TI%3D%26locale%3Den_EP; org.springframework.web.servlet.i18n.CookieLocaleResolver.LOCALE=en_EP; PGS=10; currentUrl=https%3A%2F%2Fworldwide.espacenet.com%2FsearchResults%3Fsubmitted%3Dtrue%26locale%3Den_EP%26DB%3DEPODOC%26ST%3Dadvanced%26TI%3D%26AB%3D%26PN%3D%26AP%3D%26PR%3D%26PA%3D%26IN%3D%26CPC%3D%26IC%3D%26Submit%3DSearch%26PD%3D"

dates = []
while search_date.year < 2017:
    dates.append(search_date.isoformat().replace("-", ""))
    search_date += delta
random.shuffle(dates)
f = open('dates.txt')
for line in f:
    dates.remove(line.strip())
print(len(dates))

service_args = [
    '--proxy=127.0.0.1:9150',
    '--proxy-type=socks5',
    ]

for day in dates:
    mydriver = webdriver.PhantomJS(service_args=service_args)
    url = url_base+day
    mydriver.get(search_page)
    cookies = mydriver.get_cookies()
    mydriver.delete_all_cookies()
    for cookie in cookies:
        mydriver.add_cookie(cookie)
    time.sleep(20 * (random.random() * 0.5 + 0.5))
    mydriver.get(url)

    soup = BeautifulSoup(mydriver.page_source, 'html.parser')
    # print(soup.text)

    m = re.search("(\\d*,*\\d+)\sresults found in", soup.text)
    if m is not None:
        print(day + "\t" + str(m.group(1)))
        sum += int(m.group(1).replace(",", ""))
    time.sleep(50 * (random.random() * 0.7 + 0.3))

print(sum)
