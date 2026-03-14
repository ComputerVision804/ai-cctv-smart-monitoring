import numpy as np

prev_centers = {}

def detect_fight(pid, l,t,r,b):

    cx = int((l+r)/2)
    cy = int((t+b)/2)

    if pid not in prev_centers:
        prev_centers[pid] = (cx,cy)
        return False

    px,py = prev_centers[pid]

    movement = np.sqrt((cx-px)**2 + (cy-py)**2)

    prev_centers[pid] = (cx,cy)

    if movement > 80:
        return True

    return False