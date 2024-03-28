import requests
import json
from geopy.geocoders import Nominatim
import geocoder

lat = 17.4065
lng = 78.4772

loc = Nominatim(user_agent="Geopy Library")

def address_to_latlng(place):
    # entering the location name
    getLoc = loc.geocode(place)

    # printing address
    print(getLoc.address)
    return getLoc

geoLoc = address_to_latlng("Hyderabad")

# printing latitude and longitude
print("Latitude = ", geoLoc.latitude, "\n")
print("Longitude = ", geoLoc.longitude)




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

weather = fetch_temp(geoLoc.latitude, geoLoc.longitude)
print(weather)
key = list(weather.keys())[0]
print(f"Time: {key}")
print(f"Current Temperature: {weather[key][0]}")
print(f"Humidity: {weather[key][1]}")