import datetime
import face_recognition
import cv2
import numpy 
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from sklearn.metrics import accuracy_score
from sklearn.metrics import mean_squared_error as mse
from skimage.metrics import structural_similarity as ssim

def update_known_faces():
  global known_face_encodings, known_face_names
  known_face_encodings = []
  known_face_names = []
  for filename in os.listdir(known_file_path):
    if filename.endswith(".jpg") or filename.endswith(".png"):
      image_path = os.path.join(known_file_path, filename)
      image = face_recognition.load_image_file(image_path)
      face_encoding = face_recognition.face_encodings(image)[0]  
      known_face_encodings.append(face_encoding)
      known_face_names.append(filename)

class Handler(FileSystemEventHandler):
  def on_any_event(self, event):
    if event:
      update_known_faces()  # Update faces on file change

def handle_post_request(image_data):
  global known_face_encodings, known_face_names
  image = cv2.imdecode(np.fromstring(image_data, np.uint8), cv2.IMREAD_COLOR)
  face_encoding = face_recognition.face_encodings(image)[0]  # Assuming only one face
  
  # Add the new encoding and name (based on post request data) to known lists
  known_face_encodings.append(face_encoding)
  known_face_names.append(get_name_from_post_request(image_data))  # Replace with logic to get name from post request

acc = 1
video_capture = cv2.VideoCapture(0)
known_face_encodings = []
known_face_names = []
known_file_path = "Flask\known"

# Initial loading of known faces
update_known_faces()

print(known_face_encodings, known_face_names)
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True
acclist = []

# Create observer for known folder
observer = Observer()
observer.schedule(Handler(), known_file_path, recursive=False)
observer.start()

while True:
  ret, frame = video_capture.read()
  small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
  rgb_small_frame = numpy.ascontiguousarray(small_frame[:, :, ::-1])
  if process_this_frame:

    face_locations = face_recognition.face_locations(rgb_small_frame)
    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
    face_names = []
    # print('this')
    for face_encoding in face_encodings:
      matches = face_recognition.compare_faces(known_face_encodings, face_encoding, tolerance=0.5)
      name = "Unknown"
      # print('is')
      if True in matches:
        first_match_index = matches.index(True)
        name = known_face_names[first_match_index]
        acc = ssim(known_face_encodings[first_match_index], face_encoding, data_range=1.0)
        acc = round(acc, 4)
      face_names.append(name)

      # print('not')

  process_this_frame = not process_this_frame
  for (top, right, bottom, left), name in zip(face_locations, face_names):
    top *= 4
    right *= 4
    bottom *= 4

    cv2.imshow('Video', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        print(sum(acclist)/len(acclist))
        break
