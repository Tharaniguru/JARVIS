import cv2
import os
from mtcnn import MTCNN

def save_faces(name, save_path='data/face', max_images=20):
    detector = MTCNN()
    cap = cv2.VideoCapture(0)

    count = 0
    user_folder = os.path.join(save_path, name)
    os.makedirs(user_folder, exist_ok=True)

    print(f"[INFO] Saving images to: {user_folder}")
    print("[INFO] Press 'q' to quit early")

    while count < max_images:
        ret, frame = cap.read()
        if not ret:
            break

        results = detector.detect_faces(frame)

        if results:
            x, y, w, h = results[0]['box']
            x, y = max(0, x), max(0, y)
            face = frame[y:y+h, x:x+w]

            # Save cropped face
            face_path = os.path.join(user_folder, f"{count}.jpg")
            cv2.imwrite(face_path, face)
            count += 1

            print(f"[INFO] Saved image {count}/{max_images}")

            # Draw rectangle and show count
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.putText(frame, f"{count}/{max_images}", (x, y-10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        else:
            print("[WARN] No face detected in frame.")

        cv2.imshow("Capture Faces", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


    cap.release()
    cv2.destroyAllWindows()
    print("[INFO] Face capture complete!")

if __name__ == "__main__":
    name = input("Enter your name: ")
    save_faces(name)
