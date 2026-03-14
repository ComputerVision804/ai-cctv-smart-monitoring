import numpy as np

previous_positions = {}

def detect_suspicious(track_id, x, y):

    if track_id in previous_positions:

        px,py = previous_positions[track_id]

        distance = np.sqrt((x-px)**2 + (y-py)**2)

        if distance > 80:
            return "Running"

    previous_positions[track_id] = (x,y)

    return "Normal"