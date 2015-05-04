__author__ = 'Hongyi'

from urllib.request import urlopen
import json
import sqlite3
import time
import datetime
import math
import calendar


def insert_db(data):
    cur_insert = conn.cursor()
    cur_insert.executemany("insert into temp(lat, lon, p_time, parameter, unit, aqi, category"
                           ") values ("
                           "?, ?, ?, ?, ?, ?, ?)", data)


def str_replace(s):
    return str(s).replace("\\", "\\\\").replace("'", "\\'")


def get_data(lat, lon, date, hour):
    urlbase = "http://www.airnowapi.org/aq/data/?"
    startDate = "2015-03-"
    endDate = date
    endHour = hour
    startday = datetime.datetime.strptime(date, '%Y-%m-%d')
    startday = startday + datetime.timedelta(days=-1)
    startDate = startday.strftime('%Y-%m-%d')
    startHour = hour
    parameters = "O3,PM25,PM10,CO,NO2,SO2"
    BBOX = "{0},{1},{2},{3}".format(lon - 2, lat - 2, lon + 2, lat + 2)
    # BBOX = "-129.658687,23.736257,-60.049312,50.184764"
    dataType = "A"
    format = "application/json"
    # API_KEY = "0BF2450A-6DF0-486D-AD3D-9FD8D597B7D4" # Hongyi's API
    API_KEY = "94CA2312-A005-413E-8961-053289179908"  # Yongcheng's API


    # log_name = "pollution_log_" + startDate + "T" + str(startHour) + ".txt"
    # log = open(log_name, "w")

    while True:
        try:
            url = """{0}startDate={1}T{2}&endDate={3}T{4}&parameters={5}&BBOX={6}&dataType={7}&format={8}&API_KEY={9}"""\
                  .format(urlbase, startDate, startHour, endDate, endHour, parameters, BBOX, dataType, format, API_KEY)
            response = urlopen(url).read().decode('utf-8')
            break
        except Exception as err:
            # print(str(err))
            # log.write(str(time.strftime("%d/%m %H:%M:%S", time.localtime())) + "\t" +
            #           startDate + "T" + str(startHour) + "_" +
            #           endDate + "T" + str(endHour) + "_" + ": " + str(err) + "\n")
            # log.flush()
            time.sleep(3)

    j = json.loads(response)
    data = []
    for js in j:
        lat = js['Latitude']
        lon = js['Longitude']
        p_time = str_replace(js['UTC'])
        parameter = str_replace(js['Parameter'])
        unit = str_replace(js['Unit'])
        aqi = js['AQI']
        category = js['Category']
        data.append((lat, lon, p_time, parameter, unit, aqi, category))

    insert_db(data)


def nearest_pollution_data(cur, timestamp):
    min_time_dist = 99999999999999999
    ret_aqi = -1
    for row in cur:
        p_time = row[2]
        time_st = time.strptime(p_time, "%Y-%m-%dT%H:00")
        time_dist = math.fabs(int(timestamp // 1000) - int(calendar.timegm(time_st)))
        if time_dist < min_time_dist:
            min_time_dist = time_dist
            ret_aqi = row[5]
    return ret_aqi


def dist_calc(coor1, coor2):
    # without multiplying earth radius
    lat1, lon1 = coor1
    lat2, lon2 = coor2
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = (math.sin(dlat/2)) ** 2 + math.cos(lat1) * math.cos(lat2) * (math.sin(dlon/2)) ** 2
    c = 2 * math.atan2( math.sqrt(a), math.sqrt(1-a) )
    return c


def get_pollution(lat, lon, date, hour):
    p_time = "{0}T{1}:00".format(date, hour)
    ts = int(calendar.timegm(time.strptime(p_time, "%Y-%m-%dT%H:00")))
    # get data from API and put them into database
    get_data(lat, lon, date, hour)

    # find the nearest data points
    params = ('SO2', 'NO2', 'CO', 'OZONE', 'PM2.5', 'PM10')
    poll_coor_dict = {}
    cur_search = conn.cursor()
    for param in params:
        poll_coor_dict[param] = []
        poll_coor = poll_coor_dict[param]
        cur_search.execute("SELECT DISTINCT lat, lon FROM temp WHERE parameter = '%s'" % param)
        for item in cur_search:
            poll_coor.append((float(item[0]), float(item[1])))

    poll_dict = {}
    for param in params:
        i = 0
        poll_dict[param] = -1
        poll_coor_ordered = poll_coor_dict[param][:]
        if len(poll_coor_ordered) == 0:
            continue

        poll_coor_ordered.sort(key=lambda x: dist_calc(x, (lat, lon)))
        cur2 = conn.cursor()
        while i < len(poll_coor_ordered):
            poll_lat, poll_lon = poll_coor_ordered[i]
            sql2 = """
            select *
            from temp
            where parameter = '%s' AND lat = %s AND lon = %s
            """ % (param, poll_lat, poll_lon)
            try:
                cur2.execute(sql2)
            except Exception as err:
                print(err)
                continue

            ret = nearest_pollution_data(cur2, ts)
            if ret != -1:
                poll_dict[param] = ret
                break
            i += 1
    return (poll_dict['SO2'], poll_dict['NO2'], poll_dict['OZONE'], poll_dict['PM2.5'], poll_dict['PM10'])

conn = sqlite3.connect(":memory:")
cur_create = conn.cursor()
cur_create.execute("create table temp(lat, lon, p_time, parameter, unit, aqi, category)")
