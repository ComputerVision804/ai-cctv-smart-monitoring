import time

# Dictionary to track first seen time of each person per camera
# Structure: {camera_id: {person_id: first_seen_timestamp}}
person_times = {}

# Loitering threshold in seconds
LOITERING_THRESHOLD = 12  # adjust as needed

def detect_loitering(person_id, camera_id=0):
    """
    Detect if a person is loitering in view for more than LOITERING_THRESHOLD seconds.
    Returns True if loitering detected, False otherwise.
    """

    now = time.time()

    # Initialize dictionary for camera
    if camera_id not in person_times:
        person_times[camera_id] = {}

    camera_persons = person_times[camera_id]

    # If person not seen before, set first seen timestamp
    if person_id not in camera_persons:
        camera_persons[person_id] = now
        return False

    # Calculate time spent in view
    duration = now - camera_persons[person_id]

    if duration >= LOITERING_THRESHOLD:
        return True

    return False

def reset_person(person_id, camera_id=0):
    """
    Reset the loitering timer for a person (if they leave frame or no longer suspicious)
    """
    if camera_id in person_times and person_id in person_times[camera_id]:
        del person_times[camera_id][person_id]