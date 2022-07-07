import face_recognition
import cv2
import numpy as np
from pymongo import MongoClient
from requests.exceptions import HTTPError, Timeout
import requests
import time
# client = MongoClient('localhost', 27017)

client = MongoClient("mongodb+srv://threetiersystem:Xinyxo1DIUotsoEp@cluster0.ie2a2.mongodb.net/?retryWrites=true&w=majority")

db = client['face_db']


faces = db["face"]

# This is a demo of running face recognition on live video from your webcam. It's a little more complicated than the
# other example, but it includes some basic performance tweaks to make things run a lot faster:
#   1. Process each video frame at 1/4 resolution (though still display it at full resolution)
#   2. Only detect faces in every other frame of video.

# PLEASE NOTE: This example requires OpenCV (the `cv2` library) to be installed only to read from your webcam.
# OpenCV is *not* required to use the face_recognition library. It's only required if you want to run this
# specific demo. If you have trouble installing it, try any of the other demos that don't require it instead.

BASE_URL_HARDWARE="http://threetiersystem.local:5000/api/v1"
BASE_URL_MAIN="http://threetiersystem.local:8000/api"



def recognise_face():
    # Get a reference to webcam #0 (the default one)
    video_capture = cv2.VideoCapture(2)

    # Create arrays of known face encodings and their names
    all_docs = list(faces.find({}))
    names, embeddings, ids = [doc["first_name"]
                        for doc in all_docs], [doc["embedding"] for doc in all_docs],  [doc["id"] for doc in all_docs]

    embeddings = np.array(embeddings)


    known_face_encodings = embeddings
    known_face_names = names
    known_face_ids = ids



    # Initialize some variables
    face_locations = []
    face_encodings = []
    face_names = []
    process_this_frame = True

    while True:
        # Grab a single frame of video
        ret, frame = video_capture.read()

        # Resize frame of video to 1/4 size for faster face recognition processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = small_frame[:, :, ::-1]

        # Only process every other frame of video to save time
        if process_this_frame:
            # Find all the faces and face encodings in the current frame of video
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(
                rgb_small_frame, face_locations)

            face_names = []
            for face_encoding in face_encodings:
                # See if the face is a match for the known face(s)
                matches = face_recognition.compare_faces(
                    known_face_encodings, face_encoding)
                name = "Unknown"

                # # If a match was found in known_face_encodings, just use the first one.
                # if True in matches:
                #     first_match_index = matches.index(True)
                #     name = known_face_names[first_match_index]

                # Or instead, use the known face with the smallest distance to the new face
                face_distances = face_recognition.face_distance(
                    known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)

                # use a tolarance level of 0.5 when considering best match 
                if face_distances[best_match_index] < 0.5 and matches[best_match_index]:
                    name = known_face_names[best_match_index]
                    id = known_face_ids[best_match_index]

                    video_capture.release()
                    cv2.destroyAllWindows()
                    return id

                face_names.append(name)
                

        process_this_frame = not process_this_frame

        # Display the results
        # for (top, right, bottom, left), name in zip(face_locations, face_names):
        #     # Scale back up face locations since the frame we detected in was scaled to 1/4 size
        #     top *= 4
        #     right *= 4
        #     bottom *= 4
        #     left *= 4

        #     # Draw a box around the face
        #     cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        #     # Draw a label with a name below the face
        #     cv2.rectangle(frame, (left, bottom - 35),
        #                 (right, bottom), (0, 0, 255), cv2.FILLED)
        #     font = cv2.FONT_HERSHEY_DUPLEX
        #     cv2.putText(frame, name, (left + 6, bottom - 6),
        #                 font, 1.0, (255, 255, 255), 1)

        # Display the resulting image
        cv2.imshow('Three Tier System', frame)

        # Hit 'q' on the keyboard to quit!
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release handle to the webcam
    video_capture.release()
    cv2.destroyAllWindows()



def authenticate_face_id():
    requests.post(
            f'{BASE_URL_HARDWARE}/write-to-lcd', json={'text': "Show face"})
    employee_id = recognise_face()
    print(recognise_face())
    return employee_id