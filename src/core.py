import cv2
import os

def video_stream():
    """captures a webcam stream, finds your face, makes it look cool. Hit q to quit hit b to activate
    
    
    """
    i = 0
    path = os.getcwd()
    face_cascade = cv2.CascadeClassifier(path + '/data/haarcascade_frontalface_default.xml')
    
    activate = True
    capture = cv2.VideoCapture(0)
    
    while(True):
        
        ret, frame = capture.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        faces = face_cascade.detectMultiScale(
            gray,
            scaleFactor  = 1.1,
            minNeighbors = 5,
            minSize      = (30, 30),
            flags        = cv2.CASCADE_SCALE_IMAGE
        )
        
        for (x, y, w, h) in faces:
            if activate:
                mask = frame[y:y+h+30, x:x+w+30]
                gray = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
                blur_mask = cv2.GaussianBlur(gray,(23,23),30)
                thresh = cv2.threshold(blur_mask,127,255,cv2.THRESH_BINARY_INV)[1]
                contours = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[-2]
                
                blur_for_inv = cv2.GaussianBlur(mask, (23,23), 30)
                thresh_for_inv = cv2.threshold(blur_for_inv,127,255,cv2.THRESH_BINARY_INV)[1]
                frame[y:y+blur_mask.shape[0],x:x+blur_mask.shape[1]] = thresh_for_inv
                
                for c in contours:
                    cv2.drawContours(frame, [c], 0, (0,255,0), 3)
                    cv2.drawContours(mask, [c], 0, (0, 0, 255), 3)
                
                
                cv2.circle(frame,(447,63), 63, (0,0,255), -1)
        cv2.imshow('video',frame)
        
        keyboard_input = cv2.waitKey(1) & 0xFF
        if keyboard_input == ord("b"):
            activate = not activate
        if keyboard_input == ord("q"):
            break
        
        
    capture.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    video_stream()
