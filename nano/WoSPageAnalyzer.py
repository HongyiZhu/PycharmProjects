__author__ = 'Hongyi'

from bs4 import BeautifulSoup
from urllib.request import urlopen

# Country List
country_f = open('country_wos.txt', 'r')
country_list = []
for line in country_f:
    country_list.append(line.strip())
country_f.close()

# Year range
starting = 2000
ending = 2014

# Load the page
page = urlopen("file:///C:/Users/Hongyi/Documents/GitHub/PycharmProjects/nano/J_3.html")
soup = BeautifulSoup(page)

f = open("analyze_result.txt", 'w')
for i in range(len(country_list)):
    for j in range(1, ending - starting + 2):
        print(i * (ending - starting + 1) + j)
        id_str = "set_%s_div" % str(i * (ending - starting + 1) + j)
        f.write(str(soup.find(id=id_str).text).strip() + "\t")
    f.write("\n")
f.close()






