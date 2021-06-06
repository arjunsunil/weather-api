import requests
import requests_cache
from rest_framework.response import Response
from rest_framework.exceptions import APIException

requests_cache.install_cache('weather_cache', backend='sqlite', expire_after=1800)


def get_weather_data():
    """Get weather information from third part api .cache the data and refresh the data after 30 minutes"""
    try:
        weather_list = []
        response = requests.get(url='http://api.openweathermap.org/data/2.5/find?lat=10.8505&lon=76.2711&cnt=30&appid=1945f7662872d84da0a5f6eb116715f6')
        if response.status_code == 200:
            weather_list = response.json()['list']
            return weather_list
        else:
            if "message" in response.json():
                raise Exception(response.json()['message'])
    except Exception as e:
        raise Exception(str(e))