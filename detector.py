from ultralytics import YOLO

model = YOLO("yolov8n.pt")

def detect_people(frame):

    results = model(frame)

    detections = []

    for r in results:
        for box in r.boxes:

            cls = int(box.cls[0])

            if cls == 0:  # person class

                x1,y1,x2,y2 = map(int, box.xyxy[0])
                conf = float(box.conf[0])

                detections.append([x1,y1,x2,y2,conf])

    return detections