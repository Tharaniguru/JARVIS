# collect_faces.py
import cv2
import os
import sys
from utils.embedder import get_embedding
from utils.db_handler import save_embedding


def save_faces(name, save_path='data', max_images=20):
    cap = cv2.VideoCapture(0)
    count = 0
    user_folder = os.path.join(save_path, name)
    os.makedirs(user_folder, exist_ok=True)

    print(f"[INFO] Saving images to: {user_folder}")
    print("[INFO] Press 'q' to quit early")

    while count < max_images:
        ret, frame = cap.read()
        if not ret:
            print("[ERROR] Failed to grab frame from webcam")
            break

        # Use the full frame for embedding
        face = cv2.resize(frame, (112, 112))

        face_path = os.path.join(user_folder, f"{count}.jpg")
        cv2.imwrite(face_path, face)
        print(f"[INFO] Saved image {count + 1}/{max_images} at {face_path}")

        embedding = get_embedding(face)
        if embedding is not None:
            save_embedding(name, embedding)
            print(f"[INFO] Stored embedding {count + 1}/{max_images} to DB")
        else:
            print(f"[WARN] Could not get embedding for image {count + 1}")

        count += 1
        cv2.putText(frame, f"{count}/{max_images}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.imshow("Capture Faces", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("[INFO] Manual exit requested")
            break

    cap.release()
    cv2.destroyAllWindows()
    print("[INFO] Face capture complete!")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python collect_faces.py <name>")
        sys.exit(1)

    name = sys.argv[1]
    save_faces(name)
