import tensorflow as tf
import cv2
from mtcnn import MTCNN
import numpy as np
import math

config = tf.compat.v1.ConfigProto()
config.gpu_options.allow_growth = True
session = tf.compat.v1.Session(config=config)

#print("Num GPUs Available: ", len(tf.config.list_physical_devices('GPU')))
#tf.debugging.set_log_device_placement(True)

def find_faces(img):
    """
    Find the faces in an image
    
    Parameters
    ----------
    img : Image to find faces from
   
    Returns
    -------
    faces : list of dictionaries of faces with keypoints

    """
    min_conf = 0.9
    img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    pixels = np.asarray(img)

    detector = MTCNN()

    detected = detector.detect_faces(pixels)
    faces = [i for i in detected if i['confidence'] >= min_conf]
    return faces



def get_pose_direction(faces,img_size, camera_matrix, dist_coeffs):
    """analyzes keypoints from faces and returns direction

    Args:
       faces: list dictsionaries of faces stuff
    
       img_size: img.shape

    Returns:
        list of directions

    """
    model_points = np.array([
        (0.0, 0.0, 0.0),             # Nose tip
        (-225.0, 170.0, -135.0),     # Left eye left corner
        (225.0, 170.0, -135.0),      # Right eye right corne
        (-150.0, -150.0, -125.0),    # Left Mouth corner
        (150.0, -150.0, -125.0)      # Right mouth corner
    ])
    
    p1 = []
    p2 = []
    rotation_vector_list = []
    translation_vector_list = []
    
    for face in faces:
        image_points = np.array([
            face['keypoints']['nose'],        # Nose tip
            face['keypoints']['left_eye'],    # Left eye left corner
            face['keypoints']['right_eye'],   # Right eye right corne
            face['keypoints']['mouth_left'],  # Left Mouth corner
            face['keypoints']['mouth_right']  # Right mouth corner
        ], dtype="double")
        
        
        (success, rotation_vector, translation_vector) = cv2.solvePnP(model_points, image_points, camera_matrix, dist_coeffs, flags=cv2.SOLVEPNP_UPNP)
        (nose_end_point2D, jacobian) = cv2.projectPoints(np.array([(0.0, 0.0, 1000.0)]), rotation_vector, translation_vector, camera_matrix, dist_coeffs)
        rotation_vector_list.append(rotation_vector)
        translation_vector_list.append(translation_vector)
        
        for p in image_points:
            cv2.circle(im, (int(p[0]), int(p[1])), 3, (0,0,255), -1)
      
        p1.append((int(image_points[0][0]), int(image_points[0][1])))
        p2.append((int(nose_end_point2D[0][0][0]), int(nose_end_point2D[0][0][1])))
        
    return(p1, p2, rotation_vector_list, translation_vector_list)


def iter_images(folder_path):
    """iterates through a folder and returns an attentiveness

    Args:
       folder_path: path to folder of sampled video


    """
    pass

if __name__ == '__main__':
    
    im = cv2.imread("/home/leo/Projects/ECE_Team9_Capstone/data/screenshot/screenshot-006.png")
    img_size = im.shape
    font = cv2.FONT_HERSHEY_SIMPLEX 
    focal_length = img_size[1]
    center = (img_size[1]/2, img_size[0]/2)
    camera_matrix = np.array(
        [[focal_length, 0, center[0]],
         [0, focal_length, center[1]],
         [0, 0, 1]], dtype = "double"
    )

    dist_coeffs = np.zeros((4,1)) # Assuming no lens distortion

    faces = find_faces(im)

    ang1 = []

    p1, p2, rotation_vector, translation_vector = get_pose_direction(faces, img_size, camera_matrix, dist_coeffs)
    
    j = 0
    for point1, point2 in zip(p1, p2):
        cv2.line(im, point1, point2, (255,0,0), 2)
        try:
            m = (point2[1] - point1[1]/(point2[0] - point1[0]))
            ang1.append(int(math.degrees(math.atan(m))))
        except:
            ang1.append(90)
        #cv2.putText(im, str(ang1[j])+'ang1', tuple(point1), font, 0.5, (128, 255, 255), 1)
        j+=1

    # Display image
    cv2.imshow("Output", im)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
