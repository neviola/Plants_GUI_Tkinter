import requests
import json
import random

# trenutno vrijeme HR Zagreb

# lat = 45.815
# lon = 15.9819
# part = ['minutely','alerts']

API_key = "31d3c48f05b9e58a3d90d95c052cf1de"
city_name = "Zagreb"
unit = "metric"
url_zg=f'https://api.openweathermap.org/data/2.5/weather?q={city_name}&units={unit}&appid={API_key}'


def get_current_info():
    try:
        html_json = requests.get(url_zg)
        result_json = json.loads(html_json.content)
        temp = result_json['main']['temp']          # celsius
        # kisa =  result_json['rain']['1h']         # mm

    except Exception as e:
        # ako ne radi web api daje random temperaturu zraka
        return random.randint(-50, 340 )/10
    
    return temp
    

# print(get_current_info())