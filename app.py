from flask import Flask, render_template, Response, request, redirect, url_for
from camera import CameraStream
from tracker import track_people
from loitering import detect_loitering
from fight_detection import detect_fight
from alerts import save_screenshot, start_recording, stop_recording
from heatmap import update_heatmap
from ultralytics import YOLO
import cv2
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'videos'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# -------------------------
# Camera sources (main + back)
# -------------------------
camera_sources = {
    "main": 0,  # adjust index
    "back": 1   # adjust index
}

selected_camera = "main"
current_source_path = camera_sources[selected_camera]
cams = CameraStream([current_source_path])

# Load YOLO model
model = YOLO("yolov8n.pt")
crowd_limit = 6
camera_alerts = {}

# -------------------------
# Frame generator
# -------------------------
def gen_frames():
    global cams
    while True:
        frames = cams.read_frames()
        if len(frames) == 0 or frames[0] is None:
            continue
        frame = frames[0]

        # YOLO detection
        results = model(frame)
        detections = []
        for r in results:
            for box in r.boxes:
                cls = int(box.cls[0])
                conf = float(box.conf[0])
                if cls == 0:  # person
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    detections.append(([x1, y1, x2-x1, y2-y1], conf, "person"))

        # Track people
        persons = track_people(detections, frame)
        suspicious = False

        if selected_camera not in camera_alerts:
            camera_alerts[selected_camera] = []

        for pid, l, t, r, b in persons:
            color = (0, 255, 0)
            if detect_loitering(pid):
                color = (0, 0, 255)
                suspicious = True
            if detect_fight(pid, l, t, r, b):
                color = (255, 0, 0)
                suspicious = True

            cv2.rectangle(frame, (l, t), (r, b), color, 2)
            cv2.putText(frame, f"ID {pid}", (l, t-10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

        # Crowd alert
        if len(persons) > crowd_limit:
            suspicious = True

        # Trigger alerts
        if suspicious:
            screenshot = save_screenshot(frame, camera_id=selected_camera)
            start_recording(frame, camera_id=selected_camera)
            camera_alerts[selected_camera].append(screenshot)
        else:
            stop_recording(camera_id=selected_camera)

        # Heatmap
        heatmap_path = update_heatmap(persons, frame.shape, camera_id=selected_camera)

        # Encode frame
        ret, buffer = cv2.imencode('.jpg', frame)
        if not ret:
            continue
        frame_bytes = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

# -------------------------
# Routes
# -------------------------
@app.route('/', methods=['GET', 'POST'])
def index():
    global selected_camera, current_source_path, cams

    if request.method == 'POST':
        # Camera switch
        selected_camera = request.form.get("camera_select", "main")
        current_source_path = camera_sources[selected_camera]
        cams = CameraStream([current_source_path])

        # Video upload
        if 'video_file' in request.files:
            file = request.files['video_file']
            if file.filename != '':
                path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
                file.save(path)
                current_source_path = path
                cams = CameraStream([current_source_path])
                selected_camera = 'main'  # show uploaded video as main camera
        return redirect(url_for('index'))

    return render_template('dashboard.html',
                           camera_alerts=camera_alerts,
                           selected_camera=selected_camera)

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

# -------------------------
# Run app safely
# -------------------------
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)