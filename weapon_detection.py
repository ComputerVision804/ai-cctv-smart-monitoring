from ultralytics import YOLO

weapon_model = YOLO("weapon_model.pt")

def detect_weapons(frame):

    results = weapon_model(frame)

    weapons = []

    for r in results:
        for box in r.boxes:

            cls = int(box.cls[0])
            conf = float(box.conf[0])

            x1,y1,x2,y2 = map(int, box.xyxy[0])

            label = weapon_model.names[cls]

            if label in ["knife","gun","pistol"]:
                weapons.append((label,conf,x1,y1,x2,y2))

    return weapons