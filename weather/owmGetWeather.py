__author__ = 'Hongyi'

from urllib.request import urlopen
import json
import pymysql
import time


def str_replace(s):
    return str(s).replace("\\", "\\\\").replace("'", "\\'")


def db_connect():
    return pymysql.connect(host="128.196.239.92",
                                user='shuoyu',
                                passwd="yushuo",
                                db="twitter_disease",
                                charset="utf8",
                                autocommit=True).cursor()


def get_sql(js):
    id = js["id"]
    dt = js['dt']
    name = str_replace(js['name'])
    lat = js['coord']['lat']
    lon = js['coord']['lon']
    wind_speed = js['wind']['speed']
    wind_deg = js['wind']['deg']
    clouds = js['clouds']['all']
    pressure = js['main']['pressure']
    temp = js['main']['temp']
    temp_max = js['main']['temp_max']
    temp_min = js['main']['temp_min']
    humidity = js['main']['humidity']

    w = js['weather']
    weather = str_replace(w[0]['main'])
    country = js['sys']['country']

    weather_sql = """INSERT INTO `twitter_disease`.`weather` (
        id, dt, name, lat, lon,
        wind_speed, wind_deg, clouds, pressure, temp,
        temp_max, temp_min, humidity, weather, country
        ) VALUES (
        '%s', '%s', '%s', '%s', '%s',
        '%s', '%s', '%s', '%s', '%s',
        '%s', '%s', '%s', '%s', '%s'
        )""" % (
        id, dt, name, lat, lon,
        wind_speed, wind_deg, clouds, pressure, temp,
        temp_max, temp_min, humidity, weather, country
    )
    return weather_sql


url = "http://api.openweathermap.org/data/2.5/weather?APPID=2a05e3baa14645fc29a0aefcf2553734&id="

while True:
    f = open("cityList.tsv", "r")
    i = 0
    cur = db_connect()
    log_name = "weather_log_" + str(time.strftime("%m%d%H00", time.localtime()) + ".txt")
    log = open(log_name, "w")
    for city in f.readlines():
        cityID = city.split("\t")[0]
        cityName = city.split("\t")[1]
        try:
            jsonFile = json.loads(urlopen(url+cityID).read().decode('utf-8'))
        except Exception as err:
            log.write(str(err) + "\n")
            log.flush()

        sql = get_sql(jsonFile)

        try:
            cur.execute(sql)
        except Exception as err:
            log.write(str(err) + "\n")
            log.flush()
        i += 1
        print(str(time.strftime("%d/%m %H:%M:%S", time.localtime())) + "\t" + cityName + " updated")
        if i % 100 == 0:
            time.sleep(20)
    cur.close()
    f.close()
    log.close()
    print()
    print("Update Finished for " + log_name)
    time.sleep(7200)