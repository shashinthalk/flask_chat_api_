import os
import json
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from bson import ObjectId
import ssl

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)

def create_db_connection():
    uri = os.getenv("MONGO_URI")
    client = MongoClient(
        uri, 
        server_api=ServerApi('1')
    )
    return client

def load_data_from_db():
    client = create_db_connection()
    db = client["personal_data_db"]
    collection = db['qa_data_set']
    docs = list(collection.find({}))
    json_data = json.dumps(docs, cls=JSONEncoder, indent=2)
    return json_data

def load_data_to_db():
    client = create_db_connection()
    db = client["personal_data_db"]
    collection = db['qa_data_set']
    current_dir = os.path.dirname(__file__)
    data_file_path = os.path.join(current_dir, 'qa_data.json')
    with open(data_file_path) as f:
        qa_pairs = json.load(f)
        collection.insert_many(qa_pairs)
    return True