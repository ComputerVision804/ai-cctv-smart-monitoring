import cv2
import time
import os

# Create directories if not exist
os.makedirs("static/screenshots", exist_ok=True)
os.makedirs("recordings", exist_ok=True)

# Dictionary to store video writers for multiple cameras
video_writers = {}

def save_screenshot(frame, camera_id=0):
    """
    Save a screenshot of the frame when suspicious activity is detected.
    """
    filename = f"static/screenshots/cam{camera_id}_alert_{int(time.time())}.jpg"
    cv2.imwrite(filename, frame)
    print(f"[ALERT] Screenshot saved: {filename}")
    return filename

def start_recording(frame, camera_id=0):
    """
    Start or continue recording a video for suspicious events.
    Returns the VideoWriter object for the camera.
    """
    h, w, _ = frame.shape

    if camera_id not in video_writers or video_writers[camera_id] is None:
        # Create new VideoWriter
        filename = f"recordings/cam{camera_id}_event_{int(time.time())}.avi"
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        writer = cv2.VideoWriter(filename, fourcc, 20, (w, h))
        video_writers[camera_id] = writer
        print(f"[ALERT] Started recording event video: {filename}")

    writer = video_writers[camera_id]
    writer.write(frame)
    return writer

def stop_recording(camera_id=0):
    """
    Stop recording video for the camera.
    """
    if camera_id in video_writers and video_writers[camera_id] is not None:
        video_writers[camera_id].release()
        video_writers[camera_id] = None
        print(f"[INFO] Recording stopped for camera {camera_id}")

# Optional: Telegram / Email alert template
def send_alert(message):
    """
    Placeholder function for sending alert messages via Telegram/Email.
    Implement your API keys or SMTP settings here.
    """
    print(f"[ALERT MESSAGE] {message}")
    # Example: send message via Telegram bot
    # import requests
    # token = "YOUR_TELEGRAM_BOT_TOKEN"
    # chat_id = "YOUR_CHAT_ID"
    # url = f"https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text={message}"
    # requests.get(url)