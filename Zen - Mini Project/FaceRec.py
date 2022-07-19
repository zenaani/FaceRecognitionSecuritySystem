import face_recognition
import cv2
import numpy as np


# Get a reference to webcam #0 (the default one)
video_capture = cv2.VideoCapture(0)


# Load an image of the authorised person
zen_image = face_recognition.load_image_file("Resources/Z.jpg")
zen_face_encoding = face_recognition.face_encodings(zen_image)[0]

hod_sir_image = face_recognition.load_image_file("Resources/hod_sir.jpg")
hod_sir_face_encoding = face_recognition.face_encodings(hod_sir_image)[0]

kk_sir_image = face_recognition.load_image_file("Resources/kk_sir.jpg")
kk_sir_face_encoding = face_recognition.face_encodings(kk_sir_image)[0]

princy_miss_image = face_recognition.load_image_file("Resources/princy_miss.jpg")
princy_miss_face_encoding = face_recognition.face_encodings(princy_miss_image)[0]


# Create arrays of known face encodings and their names
known_face_encodings = [
    zen_face_encoding,
    hod_sir_face_encoding,
    kk_sir_face_encoding,
    princy_miss_face_encoding
]
known_face_names = [
    "Zen",
    "Dr. Balamurugan V",
    "Dr. Krishna Kumar Kishor",
    "Dr. Princy"
]

# Intialize a list
face_names = []

while True:
    # Grab a single frame of video
    ret, frame = video_capture.read()

    # Resize frame of video to 1/4 size for faster face recognition processing
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    # Convert the image from BGR color to RGB
    rgb_small_frame = small_frame[:, :, ::-1]

    # Obtain all the faces and face encodings in the current frame of video
    face_locations = face_recognition.face_locations(rgb_small_frame)
    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

    face_names = []
    for face_encoding in face_encodings:
        # Check if the face is a match for the authorised faces
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding, tolerance= 0.5)
        name = "Unknown"

        # If a match is found open the solenoid lock
        if True in matches:
            first_match_index = matches.index(True)
            name = known_face_names[first_match_index]
            
            #response = mybolt.digitalWrite('0', 'LOW')
            #time.sleep(2)
            #response = mybolt.digitalWrite('0', 'HIGH')

        face_names.append(name)

        
    
    # Display box and label
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (255,0,100), 3)

        # Draw a label with a name below the face
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (255,0,100), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 0.75, (255, 255, 255), 1)


    # Display the video
    cv2.imshow('Video', frame)

    # Press q to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()