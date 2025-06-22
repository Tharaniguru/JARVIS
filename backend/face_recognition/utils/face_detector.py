from ultralytics import YOLO

model = YOLO("yolov8n-face-lindevs.onnx")  # Use raw string or forward slashes

def detect_faces(frame):
    results = model(frame)
    boxes = []
    for r in results:
        for box in r.boxes.xywh.cpu().numpy():
            x, y, w, h = map(int, box)
            boxes.append((x - w//2, y - h//2, w, h))  # convert center to top-left
    return boxes
