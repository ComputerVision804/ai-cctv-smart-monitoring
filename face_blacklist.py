import face_recognition
import os

known_encodings = []
known_names = []

for file in os.listdir("faces"):

    image = face_recognition.load_image_file(f"faces/{file}")
    encoding = face_recognition.face_encodings(image)[0]

    known_encodings.append(encoding)
    known_names.append(file.split(".")[0])


def detect_blacklist(frame):

    rgb = frame[:,:,::-1]

    locations = face_recognition.face_locations(rgb)
    encodings = face_recognition.face_encodings(rgb,locations)

    matches_found = []

    for face_encoding,loc in zip(encodings,locations):

        matches = face_recognition.compare_faces(
            known_encodings, face_encoding
        )

        if True in matches:

            idx = matches.index(True)
            name = known_names[idx]

            matches_found.append((name,loc))

    return matches_found