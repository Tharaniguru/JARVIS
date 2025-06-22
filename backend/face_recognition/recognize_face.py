# recognize_faces.py
import cv2
from insightface.app import FaceAnalysis
from utils.db_handler import get_all_embeddings
from utils.matcher import find_best_match

# Initialize InsightFace
app = FaceAnalysis(name='buffalo_l', providers=['CPUExecutionProvider'])
app.prepare(ctx_id=0)

def recognize_faces():
    known_faces = get_all_embeddings()
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        faces = app.get(frame)
        for face in faces:
            embedding = face.embedding
            bbox = face.bbox.astype(int)  # [x1, y1, x2, y2]
            name, score = find_best_match(embedding, known_faces)
            label = f"{name} ({score:.2f})"

            cv2.rectangle(frame, (bbox[0], bbox[1]), (bbox[2], bbox[3]), (255, 0, 0), 2)
            cv2.putText(frame, label, (bbox[0], bbox[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,0,0), 2)

        cv2.imshow("Face Recognition", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    recognize_faces()
