import cv2

def gray_video():
    """captures a webcam stream and turns it gray. Hit ESC to quit


    """
    ## TODO(#7): instead of using a webcam play video from file
    cap = cv2.VideoCapture(0) # the zero means you can capture multiple cameras
    
    while(True):
        
        ret, frame = cap.read()
        
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        cv2.imshow('frame',gray)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


    cap.release()
    cv2.destroyAllWindows()

# TODO: Clone https://github.com/tyiannak/pyAudioAnalysis.git
#       Audio analysis tool

if __name__ == '__main__':
    gray_video()

