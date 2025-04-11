from mtcnn import MTCNN
import cv2

detector = MTCNN()
cap = cv2.VideoCapture(0)

print("press q to quit.")
while True:
    ret , frame =cap.read()
    if not ret:
        break

    results = detector.detect_faces(frame)

    for face in results:
        x, y, width, height = face['box']
        confidence = face['confidence']
        keypoints = face['keypoints']

        cv2.rectangle(frame,(x,y),(x+width , y+height),(0,255,0),2)

        for point in keypoints.values():
            cv2.circle(frame, point, 2, (0, 255, 255), 2)

        cv2.putText(frame, f"{confidence:.2f}", (x, y-10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
        
    cv2.imshow("Face Detection (MTCNN)", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()