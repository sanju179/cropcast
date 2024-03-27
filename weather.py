import requests
import json
from geopy.geocoders import Nominatim
import geocoder

g = geocoder.ip('me')
print(g.latlng)
lat = g.latlng[0]
lng = g.latlng[1] 

geoloc = Nominatim(user_agent="GetLoc")

location = geoloc.reverse(f"{lat}, {lng}")
print(f"Location: {location.address}")
# sending request to api
api_url = f"https://api.tomorrow.io/v4/weather/forecast?location={lat}%2C%20{lng}&timesteps=1d&apikey=ANFakkplK6SMxJ3qANjzW6y5dAxeWi9V"
headers = {"accept": "application/json"}
# getting response
response = requests.get(api_url,headers=headers)
data = response.json()

dic = {}

daily_data = data['timelines']['daily']
for day in daily_data:
    time = day['time']
    temperature = day['values']['temperatureApparentAvg']
    humidity = day['values']['humidityAvg']
    # wind_speed = day['values']['rainfallAvg']
    
    dic[time] = [temperature, humidity]
    
print(dic)