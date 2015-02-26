__author__ = 'hzhu'

from bs4 import BeautifulSoup

queryRoot = "http://www.doctor.com/find-a-doctor?search_type=search"
s_location = "s_location=AZ"
filterDistance = "filterDistance=10"

url = queryRoot + "&" + s_location + "&" + filterDistance + "&page"

for i in range(1, 10):
    tempurl = url + str(i)
    soup = BeautifulSoup()
    print tempurl
