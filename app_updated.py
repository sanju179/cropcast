from flask import Flask, jsonify, url_for, redirect, request, render_template
import pymongo
from pymongo.server_api import ServerApi
import datetime
from model import predict_crop
from fertmodel import predict_fertilizer
from math import cos, asin, sqrt
from geopy.geocoders import Nominatim
from bson import json_util 
import json

app = Flask(__name__) 

uri = "mongodb+srv://sanjune:sanjune@cluster0.dce1pnv.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = pymongo.MongoClient(uri, server_api=ServerApi('1'))

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB ! ")
except Exception as e:
    print(e)
db = client["final"]
collection = db["recommended"]

loc = Nominatim(user_agent="Geopy Library")

@app.route('/mongo/',methods=["POST"])
def append_to_db():

    N = 104
    P = 18
    K = 30
    temperature = 43.603016
    humidity = 69.3
    ph = 6.7
    rainfall = 110.91

    crops_recommended=predict_crop(N,P,K,temperature,humidity,ph,rainfall)
    fertilizer_recommended = predict_fertilizer(N,P,K)
    collection.insert_one({
        "timestamp": datetime.datetime.now(),
    "metadata": {"sensor_id": "dht=1"},
    "temperature_in_c": f"{temperature}",
    "humidity": f"{humidity}",
    "rainfall": f"{rainfall}",
    "ph":f"{ph}",
    "n":f"{N}",
    "p":f"{P}",
    "k":f"{K}",
    'crop_prediction':crops_recommended,
    'fertilizers_rec':fertilizer_recommended
    })
    return 'Data added to MongoDB'

def distance(lat1, lon1, lat2, lon2):
    p = 0.017453292519943295
    hav = 0.5 - cos((lat2-lat1)*p)/2 + cos(lat1*p)*cos(lat2*p) * (1-cos((lon2-lon1)*p)) / 2
    return 12742 * asin(sqrt(hav))

def closest(data, v):
    min_distance = float('inf')
    closest_document = None
    
    for document in data:
        print(document)
        doc_lat = float(document['coordinates'][0])
        doc_lng = float(document['coordinates'][1])
        dist = distance(float(v['lat']), float(v['lng']), doc_lat, doc_lng)
        
        if dist < min_distance:
            min_distance = dist
            closest_document = document
        
    return closest_document


def address_to_latlng(place):
    # entering the location name
    getLoc = loc.geocode(place)

    # printing address
    print(getLoc.address)
    return getLoc

@app.route('/retrieve/',methods=["POST"])
def read_from_db():
    loc = request.form.get("value")
    location = loc.lower()

    # do location to coordinate translation here !!!

    geoLoc = address_to_latlng(location)

    lat = geoLoc.latitude
    lng = geoLoc.longitude
    # printing latitude and longitude
    print("Latitude = ", lat, "\n")
    print("Longitude = ", lng)
    curr = {'lat':lat, 'lng':lng}

    if not location:
        return jsonify({"error": "Location parameter is missing"}), 400

    cursor = collection.find()

    # Iterate over the cursor to access each document
    """ for document in cursor:
        print(document) """

    closest_data = closest(cursor, curr)
    n = closest_data['n']
    p = closest_data['p']
    k = closest_data['k']
    crops = closest_data['crop']

    all_data = { 
        'location': location,
        'closest_coordinates':[closest_data['coordinates'][0],closest_data['coordinates'][1]],
        'n': n,
        'p': p,
        'k': k,
        'common_crops': list(crops)
    }
    cursorr = json_util.dumps(all_data)
    
    return cursorr


@app.route('/')
def inital():
    return render_template("main.html")

if __name__ == "__main__":
    app.run(debug=True)