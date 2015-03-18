__author__ = 'Hongyi'

from urllib.request import urlopen
import json

f = open('cityList.tsv', 'w')

cityInUS = "http://api.openweathermap.org/data/2.5/box/city?" \
           "cluster=no&cnt=4000&format=json&bbox=-129.658687,24.378305,-63.564937,51.076736,400" \
           "&APPID=2a05e3baa14645fc29a0aefcf2553734"
jsonFile = urlopen(cityInUS).read().decode('utf-8')
cityList = []
cityList = json.loads(jsonFile)["list"]

for line in cityList:
    cityName = line['name']
    cityID = str(line['id'])
    cityCoord = line['coord']
    cityLat = str(cityCoord['lat'])
    cityLon = str(cityCoord['lon'])
    s = cityID + "\t" + cityName + "\t" + cityLat + "\t" + cityLon + "\n"
    print(s)
    f.write(s)

f.close()

