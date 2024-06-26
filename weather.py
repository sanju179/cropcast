import requests
import json
from geopy.geocoders import Nominatim
import geocoder

lat = "13.0901503"
lng = "80.1601054"

loc = Nominatim(user_agent="Geopy Library")


def address_to_latlng(place):
    # entering the location name
    getLoc = loc.geocode(place)

    # printing address
    print(getLoc.address)
    return getLoc







def fetch_temp(lat, lng):
    dic = {}
    # sending request to api
    url = "https://api.tomorrow.io/v4/weather/realtime?location=hyderabad%20&apikey=ANFakkplK6SMxJ3qANjzW6y5dAxeWi9V"

    headers = {"accept": "application/json"}
    
    response = requests.get(url, headers=headers)


    data = response.json()
    
    day = data['data']
    time = day['time']
    temperature = day['values']['temperature']
    humidity = day['values']['humidity']
        # wind_speed = day['values']['rainfallAvg']
        
    dic[time] = [temperature, humidity]
    return dic

