import datetime
import face_recognition
import cv2 
import numpy as np 
from sklearn.metrics import accuracy_score
from sklearn.metrics import mean_squared_error as mse
from skimage.metrics import structural_similarity as ssim
import smtplib, ssl
from email.message import EmailMessage
import math
camnum=1
counterr=0
def notif(msg):
    # email_sender = 'sender mail'
    # email_password = 'password'
    # email_receiver = 'receiver mail'
    email_sender = 'rushma.d.pabla@gmail.com'
    email_password = 'bdlt oevt qsnf wnud'
    email_receiver = 'rushma.dodda@gmail.com'

    # Set the subject and body of the email
    subject = 'Child Found'
    body = """
    
    """

    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = email_receiver
    em['Subject'] = subject
    em.set_content(msg)

    # Add SSL (layer of security)
    context = ssl.create_default_context()

    # Log in and send the email
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.sendmail(email_sender, email_receiver, em.as_string())
def face_distance_to_conf(face_distance, face_match_threshold=0.6):
    if face_distance > face_match_threshold:
        range = (1.0 - face_match_threshold)
        linear_val = (1.0 - face_distance) / (range * 2.0)
        return linear_val
    else:
        range = face_match_threshold
        linear_val = 1.0 - (face_distance / (range * 2.0))
        return linear_val + ((1.0 - linear_val) * math.pow((linear_val - 0.5) * 2, 0.2))
    

acc=1
video_capture = cv2.VideoCapture(0)

vinni_image = face_recognition.load_image_file("Flask\known\rush.jpg")  
vinni_face_encoding = face_recognition.face_encodings(vinni_image)[0]
shan_image = face_recognition.load_image_file("Flask\known\jaanu.jpg") 
shan_face_encoding = face_recognition.face_encodings(shan_image)[0]
known_face_encodings = [ vinni_face_encoding,shan_face_encoding]
known_face_names = [ "rush","jaanu"] 
face_locations = [] 
face_encodings = [] 
face_names = []
process_this_frame = True
acclist=[]
while True:
    ret, frame = video_capture.read()
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    rgb_small_frame = rgb_small_frame = np.ascontiguousarray(small_frame[:, :, ::-1])
    if process_this_frame:
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations) 
        face_names = []
        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding,tolerance=0.5)
            name = "Unknown"

            if True in matches:
                first_match_index = matches.index(True) 
                name = known_face_names[first_match_index] 
                # acc = accuracy_score(known_face_encodings[first_match_index], face_encoding)
                # acc=mse(known_face_encodings[first_match_index], face_encoding)
                acc=ssim(known_face_encodings[first_match_index], face_encoding)
                acc=round(acc,4)
                
            face_names.append(name)
            #print('not')
    
    process_this_frame = not process_this_frame
    for (top, right, bottom, left), name in zip(face_locations, face_names): 
        top *= 4 
        right *= 4 
        bottom *= 4 
        left *= 4
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 255, 0), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        if(name=="Unknown"):
            acc=0
            
            acclist=[1]
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            cv2.putText(frame, name , (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
        else:
            counterr=counterr+1
            cv2.putText(frame, name+" "+str(acc) , (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
            acclist.append(acc)
            
        with open('logfiles.txt', 'a') as the_file:
            stringto=name+" with ssim "+str(acc)+" was detected in camera "+str(camnum)+" at time "+str(datetime.datetime.now())+"\n"
            the_file.write(str(stringto))
        filename=name+".txt"
        with open(filename, 'a') as the_file:
            stringto=name+" with ssim "+str(acc)+" was detected in camera "+str(camnum)+" at time "+str(datetime.datetime.now())+"\n"
            the_file.write(str(stringto))
    print(counterr)
    msg="the child is found at location camera"+str(camnum)+" at time "+str(datetime.datetime.now())
    if(counterr>100):
        notif(msg)
        print(msg)
        break
        print("Notified")
    cv2.imshow('Video', frame)
    if cv2.waitKey(10) & 0xFF == ord('q'):
        print(sum(acclist)/len(acclist))
        break
video_capture.release() 
cv2.destroyAllWindows()
            
      
