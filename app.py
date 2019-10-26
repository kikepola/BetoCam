import cv2 
import sys
import time
from ftplib import FTP 
import os
import fileinput
import datetime
from urllib import request, parse
import json

def send_message_to_slack(text):    
    post = {"text": "{0}".format(text)}
 
    try:
        json_data = json.dumps(post)
        req = request.Request("https://hooks.slack.com/services/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",
                              data=json_data.encode('ascii'),
                              headers={'Content-Type': 'application/json'}) 
        resp = request.urlopen(req)
    except Exception as em:
        print("EXCEPTION: " + str(em))

def send_image_to_dash():
    ftp = FTP()
    ftp.set_debuglevel(2)
    ftp.connect('files.000webhost.com', 21) 
    ftp.login('saltless-tubes','face1223')
    localfile = 'frame.jpg'
    ftp.cwd('public_html')
    fp = open(localfile, 'rb')
    print('STOR %s' % os.path.basename(localfile))
    ftp.storbinary('STOR %s' % os.path.basename(localfile), fp, 1024)
    fp.close()
    ftp.quit()


faceCascade = cv2.CascadeClassifier('./haarcascade_frontalface_default.xml')
eyeCascade = cv2.CascadeClassifier('./haarcascade_eye.xml')
start_now = datetime.datetime.now()  
video_capture = cv2.VideoCapture(0)


while True:
    # Capture frame-by-frame
    ret, frame = video_capture.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
    )

    eye = eyeCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
    )


    
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        for (x, y, w, h) in eye:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)            
            now = datetime.datetime.now() 
            if(start_now + datetime.timedelta(minutes = 1) <= now):
                cv2.imwrite("frame.jpg", frame)  
                send_image_to_dash()
                send_message_to_slack('Sua casa esta sendo invadida')             
                start_now = now
                break
              
             

    cv2.imshow('Video', frame)  

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


video_capture.release()
cv2.destroyAllWindows()