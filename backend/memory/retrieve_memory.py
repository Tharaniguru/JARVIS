from pymongo import MongoClient
from sentence_transformers import SentenceTransformer, util
import torch


# Load the same embedding model used during storage
model = SentenceTransformer('all-mpnet-base-v2')  
# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["memory"]
collection = db["memory_logs"]

def get_similar_memory(user_input, top_k=3):
    query_embedding = model.encode(user_input, convert_to_tensor=True)

    memories = list(collection.find({}))
    if not memories:
        return []

    texts = [mem["text"] for mem in memories]  # Fix this line
    embeddings = torch.tensor([mem["embedding"] for mem in memories])

    similarity_scores = util.cos_sim(query_embedding, embeddings)[0]
    top_results = similarity_scores.topk(k=min(top_k, len(embeddings)))

    similar_memories = []
    for idx in top_results.indices:
        memory = memories[int(idx)]
        similar_memories.append({
            "text": memory["text"],
            "score": float(similarity_scores[int(idx)])
        })

    return similar_memories

if __name__ == "__main__":
    query = input("Ask something: ")
    results = get_similar_memory(query)
    if not results:
        print("No similar memories found.")
    else:
        for mem in results:
            print(f"\n🧠 Past: {mem['text']}")
            print(f"🔁 Score: {mem['score']:.2f}")
