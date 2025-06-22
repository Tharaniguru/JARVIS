from insightface.app import FaceAnalysis

app = FaceAnalysis(name='buffalo_l', providers=['CPUExecutionProvider'])
app.prepare(ctx_id=0)

def get_embedding(img):
    faces = app.get(img)
    print(f"[DEBUG] InsightFace detected {len(faces)} faces")
    if not faces:
        return None
    return faces[0].embedding

