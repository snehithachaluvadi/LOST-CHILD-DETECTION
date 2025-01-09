# import datetime
# import face_recognition
# import cv2 
# import numpy as np
# import numpy
# import os
# from sklearn.metrics import accuracy_score
# from sklearn.metrics import mean_squared_error as mse
# from skimage.metrics import structural_similarity as ssim
# import math
# camnum=1;
# counterr=0
# import smtplib, ssl
# from email.message import EmailMessage
# import math
# camnum=1
# counterr=0
# def notif(msg):
#     email_sender = 'rushma.d.pabla@gmail.com'
#     email_password = 'bdlt oevt qsnf wnud'
#     email_receiver = 'rushma.dodda@gmail.com'
#     subject = 'Child Found'
#     body = """
    
#     """
#     em = EmailMessage()
#     em['From'] = email_sender
#     em['To'] = email_receiver
#     em['Subject'] = subject
#     em.set_content(msg)
#     context = ssl.create_default_context()
#     with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
#         smtp.login(email_sender, email_password)
#         smtp.sendmail(email_sender, email_receiver, em.as_string())
# def face_distance_to_conf(face_distance, face_match_threshold=0.4):
#     if face_distance > face_match_threshold:
#         range = (1.0 - face_match_threshold)
#         linear_val = (1.0 - face_distance) / (range * 2.0)
#         return linear_val
#     else:
#         range = face_match_threshold
#         linear_val = 1.0 - (face_distance / (range * 2.0))
#         return linear_val + ((1.0 - linear_val) * math.pow((linear_val - 0.5) * 2, 0.2))
# acc=1
# video_capture = cv2.VideoCapture(0)
# known_face_encodings=[]
# known_face_names=[]
# known_file_path = "Flask\known"
# print(known_face_encodings,known_face_names)
# face_locations = [] 
# face_encodings = [] 
# face_names = []
# process_this_frame = True
# acclist=[]
# while True:
#     for filename in os.listdir(known_file_path):
#         if filename.endswith(".jpg") or filename.endswith(".png"):
#             if(filename not in  known_face_names):
#                 image_path = os.path.join(known_file_path, filename)
#                 image = face_recognition.load_image_file(image_path)
#                 face_encoding = face_recognition.face_encodings(image)[0] 
#                 known_face_encodings.append(face_encoding)
#                 known_face_names.append(filename)
#     ret, frame = video_capture.read()
#     small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
#     rgb_small_frame = numpy.ascontiguousarray(small_frame[:, :, ::-1])
#     if process_this_frame:
#         face_locations = face_recognition.face_locations(rgb_small_frame)
#         face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations) 
#         face_names = []
#         for face_encoding in face_encodings:
#             matches = face_recognition.compare_faces(known_face_encodings, face_encoding,tolerance=0.5)
#             name = "Unknown"
#             if True in matches:
#                 first_match_index = matches.index(True) 
#                 name = known_face_names[first_match_index] 
#                 acc = ssim(known_face_encodings[first_match_index], face_encoding, data_range=1.0)
#                 acc=round(acc,4)                
#             face_names.append(name)   
#     process_this_frame = not process_this_frame
#     for (top, right, bottom, left), name in zip(face_locations, face_names): 
#         top *= 4 
#         right *= 4 
#         bottom *= 4 
#         left *= 4
#         cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
#         cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 255, 0), cv2.FILLED)
#         font = cv2.FONT_HERSHEY_DUPLEX
#         if(name=="Unknown"):
#             acclist=[1]
#             cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
#             cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
#             cv2.putText(frame, name , (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
#         else:
#             counterr=counterr+1
#             cv2.putText(frame, name+" "+str(acc) , (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
#             acclist.append(acc)
            
#         with open('logfiles.txt', 'a') as the_file:
#             stringto=name+" with ssim "+str(acc)+" was detected in camera "+str(camnum)+" at time "+str(datetime.datetime.now())+"\n"
#             the_file.write(str(stringto))
#         filename=name+".txt"
#         with open(filename, 'a') as the_file:
#             stringto=name+" with ssim "+str(acc)+" was detected in camera "+str(camnum)+" at time "+str(datetime.datetime.now())+"\n"
#             the_file.write(str(stringto))     
#     print(counterr)
#     msg="the child is found at location camera"+str(camnum)+" at time "+str(datetime.datetime.now())
#     if(counterr>20):
#         notif(msg)
#         print(msg)
#         break
#         print("Notified")
#     cv2.imshow('Video', frame)
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         print(sum(acclist)/len(acclist))
#         break
# video_capture.release() 
# cv2.destroyAllWindows()

import datetime
import face_recognition
import cv2 
import numpy as np
import os
from sklearn.metrics import accuracy_score
from sklearn.metrics import mean_squared_error as mse
from skimage.metrics import structural_similarity as ssim
import math
import smtplib, ssl
from email.message import EmailMessage
from email.utils import make_msgid

# Camera and detection setup variables
camnum = 1
counterr = 0
acc = 1

# Email notification function
def notif(msg, image_path):
    email_sender = 'rushma.d.pabla@gmail.com'
    email_password = 'bdlt oevt qsnf wnud'
    email_receiver = 'rushma.dodda@gmail.com'
    subject = 'Child Found'
    
    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = email_receiver
    em['Subject'] = subject
    em.set_content(msg)

    # Add face snapshot as an attachment
    with open(image_path, 'rb') as img_file:
        em.add_attachment(img_file.read(), maintype='image', subtype='jpeg', filename='face_snip.jpg')

    # Send the email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.send_message(em)

def face_distance_to_conf(face_distance, face_match_threshold=0.4):
    if face_distance > face_match_threshold:
        range = (1.0 - face_match_threshold)
        linear_val = (1.0 - face_distance) / (range * 2.0)
        return linear_val
    else:
        range = face_match_threshold
        linear_val = 1.0 - (face_distance / (range * 2.0))
        return linear_val + ((1.0 - linear_val) * math.pow((linear_val - 0.5) * 2, 0.2))

# Initialize video capture
video_capture = cv2.VideoCapture(0)
known_face_encodings = []
known_face_names = []
known_file_path = "Flask/known"

# Load known faces
for filename in os.listdir(known_file_path):
    if filename.endswith(".jpg") or filename.endswith(".png"):
        image_path = os.path.join(known_file_path, filename)
        image = face_recognition.load_image_file(image_path)
        face_encoding = face_recognition.face_encodings(image)[0] 
        known_face_encodings.append(face_encoding)
        known_face_names.append(filename)

face_locations = [] 
face_encodings = [] 
face_names = []
process_this_frame = True
acclist = []

while True:
    ret, frame = video_capture.read()
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    rgb_small_frame = np.ascontiguousarray(small_frame[:, :, ::-1])

    if process_this_frame:
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations) 
        face_names = []

        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding, tolerance=0.5)
            name = "Unknown"
            if True in matches:
                first_match_index = matches.index(True) 
                name = known_face_names[first_match_index] 
                acc = ssim(known_face_encodings[first_match_index], face_encoding, data_range=1.0)
                acc = round(acc, 4)

            face_names.append(name)

    process_this_frame = not process_this_frame

    for (top, right, bottom, left), name in zip(face_locations, face_names):
        # Scale back up face locations
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        # If the detected face is known, save a snip of it
        if name != "Unknown":
            face_snip = frame[top:bottom, left:right]
            snip_path = f'{name}_snip.jpg'
            cv2.imwrite(snip_path, face_snip)
            counterr += 1
            acclist.append(acc)

            # Log detections
            with open('logfiles.txt', 'a') as log_file:
                log_file.write(f'{name} with SSIM {acc} was detected on camera {camnum} at {datetime.datetime.now()}\n')
            
            # Send notification after a certain threshold
            if counterr > 20:
                msg = f'The child was found at camera {camnum} at {datetime.datetime.now()}'
                notif(msg, snip_path)
                print("Notified")
                break

        # Draw rectangle and text for the detected face
        color = (0, 255, 0) if name != "Unknown" else (0, 0, 255)
        cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), color, cv2.FILLED)
        cv2.putText(frame, f"{name} {acc}", (left + 6, bottom - 6), cv2.FONT_HERSHEY_DUPLEX, 1.0, (255, 255, 255), 1)

    # Show video feed
    cv2.imshow('Video', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()
 