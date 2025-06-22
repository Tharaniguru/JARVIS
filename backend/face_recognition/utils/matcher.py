from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

def find_best_match(embedding, known_faces, threshold=0.65):
    best_match = None
    best_score = -1
    for face in known_faces:
        score = cosine_similarity([embedding], [face["embedding"]])[0][0]
        if score > best_score:
            best_score = score
            best_match = face
    if best_score >= threshold:
        return best_match["name"], best_score
    return "Unknown", best_score
