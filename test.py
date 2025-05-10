from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

uri = "mongodb+srv://nishanshashinthalive:yp9p!UDSm97bLZp@chatapp.1qjsorv.mongodb.net/?retryWrites=true&w=majority&appName=chatapp"
client = MongoClient(uri, server_api=ServerApi('1'))
db = client["sample_mflix"]
collection = db["embedded_movies"]

items = list(collection.find())
for item in items:
    item["_id"] = str(item["_id"])
print(items)