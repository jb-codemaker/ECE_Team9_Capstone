import tensorflow as tf
import cv2
from mtcnn import MTCNN
import numpy as np

config = tf.compat.v1.ConfigProto()
config.gpu_options.allow_growth = True
session = tf.compat.v1.Session(config=config)

#print("Num GPUs Available: ", len(tf.config.list_physical_devices('GPU')))
#tf.debugging.set_log_device_placement(True)


image = cv2.imread("/home/leo/Projects/ECE_Team9_Capstone/data/screenshot/screenshot-005.png")
img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
pixels = np.asarray(img)

detector = MTCNN()

results = detector.detect_faces(pixels)

for i in results:
    if i['confidence'] >= 0.9:
        print(i)
        (x,y,w,h) = i["box"]
        keypoints = i["keypoints"]
        #cv2.rectangle(image, (x,y),(x+w, y+h),(0,255,0),2)
        cv2.circle(image,(x,y),1,(0,255,0),4)
        cv2.circle(image,(x+w,y+h),1,(0,0,255),4)
        cv2.circle(image,(x+w,y),1,(255,0,0),4)
        cv2.circle(image,(x,y+h),1,(255,255,0),4)
        cv2.rectangle(image, (int(keypoints["right_eye"][0] - w*.20), int(keypoints["right_eye"][1] - h*.20)),(int(keypoints["right_eye"][0] + w*.20), int(keypoints["right_eye"][1] + h*.20)), (0,0,255),2)
       # cv2.rectangle(image, (int(keypoints["left_eye"][0] - w*.20), int(keypoints["left_eye"][1] - h*.20)),(int(keypoints["left_eye"][0] + w*.20), int(keypoints["left_eye"][1] + h*.20)), (0,0,255),2)

cv2.imshow("test",image)
cv2.waitKey(0)
cv2.destroyAllWindows()
