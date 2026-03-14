from deep_sort_realtime.deepsort_tracker import DeepSort

tracker = DeepSort(max_age=40)

def track_people(detections, frame):

    tracks = tracker.update_tracks(detections, frame=frame)

    persons = []

    for track in tracks:

        if not track.is_confirmed():
            continue

        track_id = track.track_id
        l,t,r,b = map(int, track.to_ltrb())

        persons.append((track_id,l,t,r,b))

    return persons