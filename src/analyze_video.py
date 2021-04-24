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
attentivness = []

while True:
    #get current time, increase delta and update the previous
    current = time()
    delta += current - previous
    previous = current
    
    ret, frame = cap.read()
    if ret:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        #check if 10 seconds passed
        if delta > 10:
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
                i = i+1
                cv2.putText(frame, 'face num'+str(i),(x-10,y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255), 2)
                attentivness.append(i)
            for (x, y, w, h) in frontal:
                cv2.rectangle(frame, (x,y), (x+w,y+h), (0,0,255),2)
            #cv2.imwrite("../data/test.png",frame)
            #print(str(len(profile)))
            #print(str(len(frontal)))
            #print("10 seconds")
            delta = 0
    else:
        break
    # Display the resulting frame
    #cv2.imshow('frame', frame)
  
    # This command let's us quit with the "q" button on a keyboard.
    #if cv2.waitKey(1) & 0xFF == ord('q'):
    #    break
    
  

cap.release()
#cv2.destroyAllWindows()

## analyze attentivness

#get avg attentivness
avg = sum(attentivness) / len(attentivness)
attentivness = list(map(lambda x: x/avg, attentivness))
np.savetxt("../data/attentivness.csv", attentivness, delimiter=",")
