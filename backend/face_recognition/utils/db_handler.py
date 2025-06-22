from pymongo import MongoClient
import datetime

client = MongoClient("mongodb://localhost:27017/")
db = client["face_db"]
collection = db["faces"]

def save_embedding(name, embedding):
    doc = {
        "name": name,
        "embedding": embedding.tolist(),
        "timestamp": datetime.datetime.now()
    }
    collection.insert_one(doc)

def get_all_embeddings():
    return list(collection.find())
