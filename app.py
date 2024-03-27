from flask import Flask, jsonify, url_for, redirect, request, render_template
import pymongo
from pymongo.server_api import ServerApi
import datetime

app = Flask(__name__) 

uri = "mongodb+srv://sanjune:sanjune@cluster0.dce1pnv.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = pymongo.MongoClient(uri, server_api=ServerApi('1'))

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)
db = client["trial"]
collection = db["trial"]


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
    "k":"51"
    })
    return 'Data added to MongoDB'

@app.route('/')
def inital():
    return render_template("main.html")

if __name__ == "__main__":
    app.run(debug=True)