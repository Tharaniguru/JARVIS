import os
import numpy as np
from keras_facenet import FaceNet
from PIL import Image
import pymongo
from pymongo import MongoClient

# Initialize FaceNet model
embedder = FaceNet()

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017')  # Adjust if needed
db = client['jarvis_ai']
faces_collection = db['faces']

def generate_embeddings(name, image_folder='data/', save_to_db=True):
    # Create a list to hold embeddings
    embeddings = []
    
    # Path to user's face images
    user_folder = os.path.join(image_folder, name)
    if not os.path.exists(user_folder):
        print(f"[ERROR] User folder {name} not found!")
        return

    # Process each image file
    for img_file in os.listdir(user_folder):
        img_path = os.path.join(user_folder, img_file)
        img = Image.open(img_path)
        img = img.resize((160, 160))  # Resize to FaceNet input size

        # Convert image to numpy array
        img_array = np.array(img)
        
        # Get face embedding
        embedding = embedder.embeddings([img_array])[0]
        embeddings.append(embedding)

        print(f"[INFO] Generated embedding for {img_file}")

    if save_to_db:
        # Save user embeddings to MongoDB
        user_data = {
            'name': name,
            'embeddings': embeddings
        }
        faces_collection.insert_one(user_data)
        print(f"[INFO] Saved embeddings for {name} to MongoDB")

if __name__ == "__main__":
    name = input("Enter the name of the user for embeddings: ")
    generate_embeddings(name)
