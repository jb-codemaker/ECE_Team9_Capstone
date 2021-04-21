import cv2
import os

def video_stream():
    """captures a webcam stream, finds your face, makes it look cool. Hit q to quit hit b to activate
    
    
    """
    face_cascade = cv2.CascadeClassifier('/home/leo/Projects/ECE_Team9_Capstone/data/haarcascade_frontalface_default.xml')
    profile_cascade = cv2.CascadeClassifier('/home/leo/Projects/ECE_Team9_Capstone/data/haarcascade_profileface.xml')
    capture = cv2.VideoCapture("/home/leo/Projects/ECE_Team9_Capstone/data/output.mp4")
    
    while(True):
        
        ret, frame = capture.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        profile = profile_cascade.detectMultiScale(
            gray,
            scaleFactor  = 1.1,
            minNeighbors = 5,
            minSize      = (30, 30),
            flags        = cv2.CASCADE_SCALE_IMAGE
        )
        
        faces = face_cascade.detectMultiScale(
            gray,
            scaleFactor  = 1.1,
            minNeighbors = 5,
            minSize      = (30, 30),
            flags        = cv2.CASCADE_SCALE_IMAGE
        )
        
        i = 0
        for (x, y, w, h) in profile:
            cv2.rectangle(frame, (x,y), (x+w,y+h), (0,255,0),2)
            i = i+1
            cv2.putText(frame, 'face num'+str(i),(x-10,y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255), 2)
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x,y), (x+w,y+h), (0,0,255),2)
            
        cv2.imshow('video',frame)
        
        keyboard_input = cv2.waitKey(1) & 0xFF
        if keyboard_input == ord("q"):
            break
        
        
    capture.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    video_stream()
