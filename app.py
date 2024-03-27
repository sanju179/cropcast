from flask import Flask, jsonify, url_for, redirect, request, render_template
import pymongo
from pymongo.server_api import ServerApi
import datetime
from bson import json_util 
import json

app = Flask(__name__) 

uri = "mongodb+srv://sanjune:sanjune@cluster0.dce1pnv.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = pymongo.MongoClient(uri, server_api=ServerApi('1'))

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)
db = client["test"]
collection = db["test"]


@app.route('/mongo/',methods=["POST"])
def append_to_db():
    

    collection.insert_one({
        "timestamp": datetime.datetime.now(),
    "metadata": {"sensor_id": "dht=1"},
    "temperature_in_c": "30",
    "temperature_in_f": "86",
    "humidity": "45",
    "rainfall": "110",
    "n":"60",
    "p":"43",
    "k":"51",
    "crop":"coffee",
    "latitude":"23.4",
    "longitude":"45.6",
    "location":"chennai"
    })
    collection.insert_one({
        "timestamp": datetime.datetime.now(),
    "metadata": {"sensor_id": "dht=1"},
    "temperature_in_c": "30",
    "temperature_in_f": "86",
    "humidity": "45",
    "rainfall": "110",
    "n":"50",
    "p":"63",
    "k":"59",
    "crop":"tea",
    "latitude":"13.4",
    "longitude":"45.8",
    "location":"mumbai"
    })
    collection.insert_one({
        "timestamp": datetime.datetime.now(),
    "metadata": {"sensor_id": "dht=1"},
    "temperature_in_c": "34",
    "temperature_in_f": "86",
    "humidity": "45",
    "rainfall": "110",
    "n":"50",
    "p":"63",
    "k":"59",
    "crop":"tea",
    "latitude":"83.4",
    "longitude":"45.8",
    "location":"chennai"
    })
    return 'Data added to MongoDB'

@app.route('/retrieve/',methods=["POST"])
def read_from_db():
    loc = request.form.get("value")
    location = loc.lower()
    if not location:
        return jsonify({"error": "Location parameter is missing"}), 400

    data = collection.find({"location":location})

    n_values = []
    p_values = []
    k_values = []
    crops = set()
    for entry in data:
        n_values.append(int(entry.get('n', 0)))
        p_values.append(int(entry.get('p', 0)))
        k_values.append(int(entry.get('k', 0)))
        crops.add(entry.get('crop', 'Unknown'))
    
    if not n_values:
        return jsonify({"error": f"No data found for location '{location}'"}), 404
    
    avg_n = sum(n_values) / len(n_values)
    avg_p = sum(p_values) / len(p_values)
    avg_k = sum(k_values) / len(k_values)
    
    # Return results as JSON
    all_data = {
        'location': location,
        'average_n': avg_n,
        'average_p': avg_p,
        'average_k': avg_k,
        'common_crops': list(crops)
    }
    cursor = json_util.dumps(all_data)
    return cursor

@app.route('/')
def inital():
    return render_template("main.html")

if __name__ == "__main__":
    app.run(debug=True)