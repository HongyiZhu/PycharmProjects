__author__ = 'Hongyi'

import weather_realtime
import pollution_realtime


def get_api_return(lat, lon, date, hour):
    weather = weather_realtime.get_weather_json(lat, lon)
    pollution = pollution_realtime.get_pollution(lat, lon, date, hour)
    string = ""
    for item in weather:
        string += str(item)
        string += ", "
    for item in pollution:
        string += str(item)
        string += ", "
    string += "?"

    return string

# print(get_api_return(32.2217, -110.9264, "2015-5-3", 16))