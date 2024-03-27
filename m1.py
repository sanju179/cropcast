import datetime

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

uri = "mongodb+srv://sanjune:sanjune@cluster0.dce1pnv.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

db = client["trial"]
collection = db["trial"]

collection.insert_one({
      "timestamp": datetime.datetime.now(),
"metadata": {"sensor_id": "dht=1"},
"temperature_in_c": "30",
"temperature_in_f": "86",
"humidity": "45",
"heat_index_in_c": "75",
"heat_index_in_f": "95"
   })