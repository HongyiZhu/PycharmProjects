
from urllib.request import urlopen
import json
import pymysql
import time
from socket import timeout


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
    lat = js['Latitude']
    lon = js['Longitude']
    p_time = str_replace(js['UTC'])
    parameter = str_replace(js['Parameter'])
    unit = str_replace(js['Unit'])
    aqi = js['AQI']
    category = js['Category']

    pollution_sql = """INSERT INTO `twitter_disease`.`pollution` (
        lat, lon, p_time, parameter,
        unit, aqi, category
        ) VALUES (
        '%s', '%s', '%s', '%s', '%s',
        '%s', '%s'
        )""" % (
        lat, lon, p_time, parameter, unit, aqi, category
    )
    return pollution_sql


urlbase = "http://www.airnowapi.org/aq/data/?"
startDate = "2015-03-"
startDay = 20
startHour = 0
endDate = "2015-03-"
endDay = 31
endHour = 23
parameters = "O3,PM25,PM10,CO,NO2,SO2"
BBOX = "-129.658687,23.736257,-60.049312,50.184764"
dataType = "A"
format = "application/json"
API_KEY = "94CA2312-A005-413E-8961-053289179908"

# http://www.airnowapi.org/aq/data/?startDate=2015-03-19T03&endDate=2015-03-19T04&parameters=O3,PM25,PM10,CO,NO2,SO2&BBOX=-129.658687,23.736257,-60.049312,50.184764&dataType=A&format=text/csv&API_KEY=

while True:
    cur = db_connect()
    print("Database connected")
    log_name = "log/pollution_log_" + startDate + str(startDay) + "T" + str(startHour) + ".txt"
    log = open(log_name, "w")
    for i in range(0, 24):
        startHour -= 1
        endHour -= 1
        if startHour == -1:
            startHour = 23
            startDay -= 1
        if endHour == -1:
            endHour = 23
            endDay -= 1
        try:
            url = """{0}startDate={1}{2}T{3}&endDate={4}{5}T{6}&parameters={7}&BBOX={8}&dataType={9}&format={10}&API_KEY={11}"""\
                .format(urlbase, startDate, startDay, startHour, endDate, endDay,
                        endHour, parameters, BBOX, dataType, format, API_KEY)
            response = urlopen(url).read().decode('utf-8')
            j = json.loads(response)
            print("Query " + startDate + str(startDay) + "T" + str(startHour) + "_" +
                  endDate + str(endDay) + "T" + str(endHour) + " succeeded")
            for item in j:
                sql = get_sql(item)
                try:
                    cur.execute(sql)
                except Exception as err:
                    log.write(str(err) + "\n")
                    log.flush()
        except Exception as err:
            # print(str(err))
            log.write(str(time.strftime("%d/%m %H:%M:%S", time.localtime())) + "\t" +
                      startDate + str(startDay) + "T" + str(startHour) + "_" +
                      endDate + str(endDay) + "T" + str(endHour) + "_" + ": " + str(err) + "\n")
            log.flush()
            continue

        print(str(time.strftime("%d/%m %H:%M:%S", time.localtime())) + "\t" + " updated")
    cur.close()
    log.close()
    print()
    print("Update Finished for " + log_name)

    time.sleep(300)