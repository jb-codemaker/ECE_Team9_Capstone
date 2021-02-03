import cv2

def gray_video(video_file_path):
    """takes a video and returns a gray version of it
    
    Args:
       video_file_path: path to video
    
    
    """
    
    cap = cv2.VideoCapture(video_file_path)
    
    while(cap.isOpened()):
        
        ret, frame = cap.read()
        
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        cv2.imshow('frame',gray)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    gray_video('/home/leo/Data/2021-02-02 21-35-04.mkv')

