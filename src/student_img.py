import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '1'
import numpy as np
import utils
import cv2
import random
from math_funcs import make_vect, get_magnitude
from student_funcs import get_angle
from classes import Student
import tensorflow as tf
from mtcnn import MTCNN

config = tf.compat.v1.ConfigProto()
config.gpu_options.allow_growth = True
session = tf.compat.v1.Session(config=config)

print("Num GPUs Available: ", len(tf.config.list_physical_devices('GPU')))
# tf.debugging.set_log_device_placement(True)

debug = False
if debug:
    pinocchio = 0
    delimiter = utils.get_delimiter()
    debug_dir = utils.get_screenshot_dir() + delimiter + 'debug' + delimiter + 'face_analyzer'
    if not os.path.exists(debug_dir):
        os.makedirs(debug_dir)
        

def find_student_next_frame(student, next_image):
    """finds student in next frame and updates student attributes

    Args:
       student: student object 
       next_image: image for next frame

    """
    top_left_point = (student.face_points['left_eye'][0], student.face_points['left_eye'][1])
    bottom_right_point = (student.face_points['mouth_right'][0], student.face_points['mouth_right'][1])
    
    student_box = utils.extend_box(top_left_point, bottom_right_point, 50)
    
    mask = np.zeros(next_image.shape[:2], dtype=np.uint8)
    mask[student_box[0][1]:student_box[1][1]+1, student_box[0][0]:student_box[1][0]+1] = 255
    rect_img = cv2.bitwise_and(next_image, next_image, mask=mask)
    
    face = find_faces(rect_img)
    if len(face) > 1:
        # TODO(#17): find a way to decrease dx and call function again
        # print("more faces")
        
        student.attention_angle_list.append(random.randint(1, 359))
    if len(face) < 1:
        # if no face append with noise
        # print("no face")
        student.attention_angle_list.append(random.randint(1, 359))
        student.absent_from_frame += 1
            
    if len(face) == 1:
        student.update_face = face[0]
        get_pose_direction(student, next_image)
        get_angle(student)
        student.absent_from_frame = 0


def find_new_students(student_list, next_frame, index):
    """looks for new students and appends them to student_list

    Args:
       student_list: list of objects
       next_frame: next image
       index: the index of the frame

    Returns:
        student_list

    """
    faces = find_faces(next_frame)
    for face in faces:
        
        found = False
        top_left = face['keypoints']['left_eye']
        bottom_right = face['keypoints']['mouth_right']
        box = utils.extend_box(top_left, bottom_right, 50)
        
        for student in student_list:
            test_point = student.face_points['nose']
            
            # cv2.circle(img, test_top_left,1,(0,0,255),2)
            # cv2.circle(img, test_bottom_right,1,(0,0,255),2)
            # cv2.rectangle(img, extended_top_left, extended_bottom_right, (255,255,0),1)
            # utils.show_image(img)

            if utils.point_in_box(box, test_point):
                found = True
                break
                        
        if not found:
            max_name = max([int(x.name) + 1 for x in student_list])
            attention_list = [random.randint(1, 359) for i in range(index + 1)]
            student_list.append(Student(face, max_name))
            student_list[-1].attention_angle_list = attention_list

def get_pose_direction(student,img):
    """makes a vector out of 2 points

    Args:
       Student: student object
       img: frame

    """
    img_size = img.shape
    focal_length = img_size[1]
    center = (img_size[1]/2, img_size[0]/2)
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
    dist_coeffs = np.zeros((4, 1))
    image_points = np.array([
        student.face_points['nose'],        
        student.face_points['left_eye'],    
        student.face_points['right_eye'],   
        student.face_points['mouth_left'],  
        student.face_points['mouth_right']  
    ], dtype="double")
    (success, rotation_vector, translation_vector) = cv2.solvePnP(model_points, image_points, camera_matrix, dist_coeffs, flags=cv2.SOLVEPNP_UPNP)

    (nose_end_point2D, jacobian) = cv2.projectPoints(np.array([(0.0, 0.0, 1000.0)]), rotation_vector, translation_vector, camera_matrix, dist_coeffs)

    student.attention_points = ((int(image_points[0][0]), int(image_points[0][1])), (int(nose_end_point2D[0][0][0]), int(nose_end_point2D[0][0][1])))

    # make a reference line
    vect = make_vect(student.attention_points[0], student.attention_points[1])
    
    d = get_magnitude(vect)

    student.reference_points = ((int(image_points[0][0]), int(image_points[0][1])), (int(image_points[0][0] + d), int(image_points[0][1])))
    
    global debug
    if debug:
        global pinocchio
        global debug_dir
        global delimiter
        
        cv2.line(img, student.attention_points[0], student.attention_points[1], (255, 0, 0), 2)
        cv2.line(img, student.reference_points[0], student.reference_points[1], (0, 255, 0), 2)
        cv2.imwrite(debug_dir + delimiter + 'pinocchio-'+str(pinocchio)+'.jpg', img)
        pinocchio += 1

def find_faces(img):
    """Find the faces in an image

    Args:
       img: Image to find faces from

    Returns:
        list of dictionaries of faces with keypoints

    """
    min_conf = 0.9
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    pixels = np.asarray(img)

    detector = MTCNN()

    detected = detector.detect_faces(pixels)
    faces = [i for i in detected if i['confidence'] >= min_conf]
    return faces


def initial_frame(img):
    """initializes student object

    Args:
       img: first image in directory

    Returns:
        list of student objects

    """
    student_list = []
    faces = find_faces(img)
    for i in range(len(faces)):
        student_list.append(Student(faces[i],str(i)))

    for student in student_list:
        get_pose_direction(student,img)
        get_angle(student)
    return student_list
