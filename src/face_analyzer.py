import tensorflow as tf
import cv2
from mtcnn import MTCNN
import numpy as np
import math
import os

config = tf.compat.v1.ConfigProto()
config.gpu_options.allow_growth = True
session = tf.compat.v1.Session(config=config)

# print("Num GPUs Available: ", len(tf.config.list_physical_devices('GPU')))
# tf.debugging.set_log_device_placement(True)

class student:
    
    def __init__(self, face, name, img_size):
        self.face = face
        self.name = name
        self.img_size = img_size
        self.box = face['box']
        self.face_points = face['keypoints']
        
    def __repr__(self):
        return "student('{}', '{}')".format(self.box, self.name)

    
    def get_pose_direction(self):
        focal_length = self.img_size[1]
        center = (self.img_size[1]/2, self.img_size[0]/2)
        camera_matrix = np.array(
        [[focal_length, 0, center[0]],
         [0, focal_length, center[1]],
         [0, 0, 1]], dtype = "double"
    )
        model_points = np.array([
            (0.0, 0.0, 0.0),             # Nose tip
            (-225.0, 170.0, -135.0),     # Left eye left corner
            (225.0, 170.0, -135.0),      # Right eye right corne
            (-150.0, -150.0, -125.0),    # Left Mouth corner
            (150.0, -150.0, -125.0)      # Right mouth corner
        ])
        dist_coeffs = np.zeros((4,1))
        image_points = np.array([
            self.face_points['nose'],        
            self.face_points['left_eye'],    
            self.face_points['right_eye'],   
            self.face_points['mouth_left'],  
            self.face_points['mouth_right']  
        ], dtype="double")
        (success, rotation_vector, translation_vector) = cv2.solvePnP(model_points, image_points, camera_matrix, dist_coeffs, flags=cv2.SOLVEPNP_UPNP)
        
        (nose_end_point2D, jacobian) = cv2.projectPoints(np.array([(0.0, 0.0, 1000.0)]), rotation_vector, translation_vector, camera_matrix, dist_coeffs)

        #for p in image_points:
        #    cv2.circle(im, (int(p[0]), int(p[1])), 3, (0, 0, 255), -1)
      
        p1 = (int(image_points[0][0]), int(image_points[0][1]))
        p2 = (int(nose_end_point2D[0][0][0]), int(nose_end_point2D[0][0][1]))
        return (p1, p2)
    
    
    
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
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    pixels = np.asarray(img)

    detector = MTCNN()

    detected = detector.detect_faces(pixels)
    faces = [i for i in detected if i['confidence'] >= min_conf]
    return faces



def iter_images(folder_path):
    """iterates through a folder and returns an attentiveness

    Args:
       folder_path: path to folder of sampled video


    """
    os.chdir(folder_path)
    for filename in os.listdir(folder_path):
        print(filename)
        im = cv2.imread(filename)
        img_size = im.shape
        faces = find_faces(im)
        student_list = []
        for i in range(len(faces)):
            student_list.append(student(faces[i], str(i), img_size))

        for i in student_list:
            student_pose = i.get_pose_direction()
            cv2.line(im, student_pose[0], student_pose[1], (255, 0, 0), 2)
            
        cv2.imshow("output",im)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    os.chdir(os.path.relpath("../../src/"))

# TODO(#13): get_angle function, make a function to get an angle for a particular student
# TODO: get_mode_angle, make a function get most common angle
# TODO: check_if_same_student, make a function that returns true if the student is the same, then appends angle to list of angles
# TODO: attentiveness_for_frame, gets the ratio of current angle for frame / mode angle
if __name__ == '__main__':
    if os.name == 'posix':
        delimiter = '/'
    else: 
        delimiter = '\\'
    current_directory = os.getcwd()
    data_directory = os.path.abspath(os.path.join(current_directory, os.pardir + delimiter + 'data'))
    screenshot_directory = os.path.abspath(os.path.join(data_directory + delimiter + 'screenshot'))

    iter_images(screenshot_directory)
    
    # j = 0
    # for point1, point2 in zip(p1, p2):
    #     cv2.line(im, point1, point2, (255, 0, 0), 2)
    #     try:
    #         m = (point2[1] - point1[1]/(point2[0] - point1[0]))
    #         ang1.append(int(math.degrees(math.atan(m))))
    #     except:
    #         ang1.append(90)
    #     #cv2.putText(im, str(ang1[j])+'ang1', tuple(point1), font, 0.5, (128, 255, 255), 1)
    #     j+= 1

    # Display image
    #cv2.imshow("Output", im)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows() 
