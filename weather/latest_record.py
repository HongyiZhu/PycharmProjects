__author__ = 'Hongyi'

import time
import calendar
import math


def nearest_pollution_data(cur, timestamp):
    min_time_dist = 99999999999999999
    ret_aqi = -1
    for row in cur:
        p_time = row[2]
        time_st = time.strptime(p_time, "%Y-%m-%dT%H")
        time_dist = math.fabs(int(timestamp // 1000) - int(calendar.timegm(time_st)))
        if time_dist < min_time_dist:
            min_time_dist = time_dist
            ret_aqi = row[5]
    return ret_aqi
