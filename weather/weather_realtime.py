__author__ = 'Hongyi'

from urllib.request import urlopen
import json
import time


def str_replace(s):
    return str(s).replace("\\", "\\\\").replace("'", "\\'")


def get_val(js):
    dt = js['dt']
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

    return (wind_speed, wind_deg, clouds, pressure, temp, humidity, weather)


url = "http://api.openweathermap.org/data/2.5/weather?APPID=2a05e3baa14645fc29a0aefcf2553734&"


def get_weather_json(lat, lon):
    loc_str = "lat=" + str(lat) + "&lon=" + str(lon)
    while True:
        try:
            response = urlopen(url+loc_str).read().decode('utf-8')
            jsonFile = json.loads(response)
            # print(json.dumps(jsonFile,indent=4))
            val = get_val(jsonFile)
            break
        except Exception as err:
            time.sleep(3)
    return val
# print(get_weather_json(32.2217, -110.9264))