__author__ = 'Hongyi'

import math


def calc_weather_dist(pair, city_list):
    min_dist = 999999
    min_lat = 0
    min_lon = 0
    for city in city_list:
        lat = city[0]
        lon = city[1]
        if math.sqrt(math.pow((lat - pair[0]), 2) + math.pow((lon - pair[1]), 2)) < min_dist:
            min_dist = math.sqrt(math.pow((lat - pair[0]), 2) + math.pow((lon - pair[1]), 2))
            min_lat = lat
            min_lon = lon
    return min_lat, min_lon


print(calc_weather_dist((1, 0), [(0, 1), (1, 1), (2, 1)]))