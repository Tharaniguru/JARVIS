# backend/memory/store_message.py

from sentence_transformers import SentenceTransformer
from pymongo import MongoClient
from datetime import datetime
import numpy as np

# Load embedding model (offline)
model = SentenceTransformer('all-mpnet-base-v2')  # First time it'll download, then cached

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["memory"]
memory_collection = db["memory_logs"]

def store_message(text, speaker="user", type="general"):
    # Convert text to embedding
    embedding = model.encode(text).tolist()

    # Create memory document
    doc = {
        "text": text,
        "embedding": embedding,
        "timestamp": datetime.utcnow(),
        "speaker": speaker,
        "type": type
    }

    # Insert into DB
    memory_collection.insert_one(doc)
    print(f"[MEMORY] Stored message: '{text}'")

# Example usage
if __name__ == "__main__":
    user_input = input("Enter message to store: ")
    store_message(user_input)
