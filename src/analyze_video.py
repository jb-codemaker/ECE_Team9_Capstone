import cv2
import numpy as np
from time import time




cap = cv2.VideoCapture("../data/output.mp4")

# initialize time
previous = time()
delta = 0

#cascade detector
frontal_cascade = cv2.CascadeClassifier("../data/haarcascade_frontalface_default.xml")
profile_cascade = cv2.CascadeClassifier("../data/haarcascade_profileface.xml")
eye_cascade = cv2.CascadeClassifier("../data/haarcascade_eye.xml")


while True:
    #get current time, increase delta and update the previous
    current = time()
    delta += current - previous
    previous = current
    
    ret, frame = cap.read()
  
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    #check if 10 seconds passed
    if delta > 3:
        i = 0
        profile = profile_cascade.detectMultiScale(
            gray,
            scaleFactor  = 1.1,
            minNeighbors = 5,
            minSize      = (30, 30),
            flags        = cv2.CASCADE_SCALE_IMAGE
            
        )

        frontal = frontal_cascade.detectMultiScale(
            gray,
            scaleFactor  = 1.1,
            minNeighbors = 5,
            minSize      = (30, 30),
            flags        = cv2.CASCADE_SCALE_IMAGE
            
        )

        for (x, y, w, h) in profile:
            cv2.rectangle(frame, (x,y), (x+w,y+h), (0,255,0),2)
            roi_gray = gray[y:y+h, x:x+w]
            roi_color = frame[y:y+h, x:x+w]
            eyes = eye_cascade.detectMultiScale(roi_gray)
            for (ex,ey,ew,eh) in eyes:
                cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
        for (x, y, w, h) in frontal:
            i = i+1
            cv2.putText(frame, 'face num'+str(i),(x-10,y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255), 2)
            cv2.rectangle(frame, (x,y), (x+w,y+h), (0,0,255),2)
            roi_gray = gray[y:y+h, x:x+w]
            roi_color = frame[y:y+h, x:x+w]
            eyes = eye_cascade.detectMultiScale(roi_gray)
            for (ex,ey,ew,eh) in eyes:
                cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
        cv2.imwrite("../data/test.png",frame)
        print(str(len(profile)))
        print(str(len(frontal)))
        print("10 seconds")
        delta = 0

    # Display the resulting frame
    cv2.imshow('frame', frame)
  
    # This command let's us quit with the "q" button on a keyboard.
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
  
  
# Release the capture and destroy the windows
cap.release()
cv2.destroyAllWindows()
