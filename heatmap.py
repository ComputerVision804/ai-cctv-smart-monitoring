# heatmap.py
import numpy as np
import cv2
import os

HEATMAP_DIR = "static/heatmaps"
os.makedirs(HEATMAP_DIR, exist_ok=True)

# Store heatmap per camera
heat_data = {}

def update_heatmap(persons, frame_shape, camera_id=0):
    """
    Update heatmap for each camera
    """
    global heat_data

    h, w, _ = frame_shape

    if camera_id not in heat_data:
        heat_data[camera_id] = np.zeros((h, w), dtype=np.float32)

    for _, l, t, r, b in persons:
        cx = int((l + r) / 2)
        cy = int((t + b) / 2)
        # increment small area
        heat_data[camera_id][max(cy-2,0):cy+3, max(cx-2,0):cx+3] += 1

    # Convert to heatmap image
    heatmap_img = cv2.applyColorMap(np.uint8(np.minimum(heat_data[camera_id]*25, 255)), cv2.COLORMAP_JET)

    # Save heatmap image
    path = os.path.join(HEATMAP_DIR, f"heatmap_cam{camera_id}.jpg")
    cv2.imwrite(path, heatmap_img)
    return path