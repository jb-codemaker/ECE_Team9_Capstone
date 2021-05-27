import tensorflow as tf
import cv2
from mtcnn import MTCNN
import numpy as np
import math
from utils import extend_box, point_in_box, show_image
import os
import logging

logging.getLogger('tensorflow').disabled = True

config = tf.compat.v1.ConfigProto()
config.gpu_options.allow_growth = True
session = tf.compat.v1.Session(config=config)

# print("Num GPUs Available: ", len(tf.config.list_physical_devices('GPU')))
# tf.debugging.set_log_device_placement(True)

class Student:
    
    def __init__(self, face, name):
        self.face = face
        self.name = name
        self.box = face['box']
        self.face_points = face['keypoints']
        self.attention_points = (0,0)
        self.attention_angle_list = []
        self.mode_attention_angle = 0
        self.attention_angle_per_frame = []
        self.absent_from_frame = 0

    @property
    def update_face(self):
       self.face = face
       self.box = face['box']
       self.face_points = face['keypoints']

    @update_face.setter
    def update_face(self, face):
        self.face = face
        self.box = face['box']
        self.face_points = face['keypoints']
        
    def __repr__(self):
        return "student('{}', '{}')".format(self.box, self.name)

    def __str__(self):
        return "student: {} attentiveness: {}".format(self.name, self.attention_angle_list)

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

def get_pose_direction(student,im):
    img_size = im.shape
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
    dist_coeffs = np.zeros((4,1))
    image_points = np.array([
        student.face_points['nose'],        
        student.face_points['left_eye'],    
        student.face_points['right_eye'],   
        student.face_points['mouth_left'],  
        student.face_points['mouth_right']  
    ], dtype="double")
    (success, rotation_vector, translation_vector) = cv2.solvePnP(model_points, image_points, camera_matrix, dist_coeffs, flags=cv2.SOLVEPNP_UPNP)
    
    (nose_end_point2D, jacobian) = cv2.projectPoints(np.array([(0.0, 0.0, 1000.0)]), rotation_vector, translation_vector, camera_matrix, dist_coeffs)

    # for p in image_points:
    #     cv2.circle(im, (int(p[0]), int(p[1])), 3, (0, 0, 255), -1)
      
    student.attention_points = ((int(image_points[0][0]), int(image_points[0][1])),(int(nose_end_point2D[0][0][0]), int(nose_end_point2D[0][0][1])))



def initial_frame(img):
    """initializes student object

    Args:
       img: first image in directory

    Returns:
        list of student objects

    """
    student_list = []
    img_size = img.shape
    faces = find_faces(img)
    for i in range(len(faces)):
        student_list.append(Student(faces[i],str(i)))

    for student in student_list:
        get_pose_direction(student,img)
        get_angle(student)
    return student_list


def find_student_next_frame(student, next_image):
    """finds student in next frame and updates student attributes

    Args:
       student: student object 
       next_image: image for next frame

    """
    top_left_point = (student.face_points['left_eye'][0], student.face_points['left_eye'][1])
    bottom_right_point = (student.face_points['mouth_right'][0], student.face_points['mouth_right'][1])
    
    student_box = extend_box(top_left_point, bottom_right_point, 50)
    
    mask = np.zeros(next_image.shape[:2], dtype=np.uint8)
    mask[student_box[0][1]:student_box[1][1]+1,student_box[0][0]:student_box[1][0]+1] = 255
    rect_img = cv2.bitwise_and(next_image,next_image,mask=mask)
    
    face = find_faces(rect_img)
    if len(face) > 1:
        # TODO(#17): find a way to decrease dx and call function again
        #print("more faces")
        
        # TODO(#20): add noise here instead of zero
        student.attention_angle_list.append(0)
    if len(face) < 1:
        #if no faceappend with noise
        #print("no face")
        student.attention_angle_list.append(0)
        student.absent_from_frame += 1
            
    if len(face) == 1:
        student.update_face = face[0]
        get_pose_direction(student,next_image)
        get_angle(student)
        # lets test this out
        student.absent_from_frame = 0

    # show_image(rect_img)
    #return student

    
def get_angle(student):
    """gets the angle of the slope of the points (best we could do), appends that angle to angle list

    Args:
       student: thestudent working on
    """
    attention_points = student.attention_points
    try:
        m = ((attention_points[1][1] - attention_points[0][1])/(attention_points[1][0] - attention_points[0][0]))
        angle = int(math.degrees(math.atan(m)))
        student.attention_angle_list.append(angle)
    except ZeroDivisionError:
        angle = -90
        student.attention_angle_list.append(angle)

def get_mode_angle(student):
    """gets the mode angle (students are assumed to be paying attention most of the time)

    Args:
       student: student object


    """
    angle_list = student.attention_angle_list
    
    # filter out value for zero
    for i in range(len(angle_list)):
        if abs(angle_list[i]) <= 2:
            if angle_list[i] > 0:
                angle_list[i] = 3
            else:
                angle_list[i] = -3
            
    binned = [5 * round(x/5) for x in angle_list]
    mode = max(set(binned), key=binned.count)
    student.mode_attention_angle = mode
    

def get_attention_per_frame(student):
    """gets the ratio of the attention at frame vs mode_attention_angle

    Args:
       student: student object


    """
    attention_list = student.attention_angle_list
    mode_attention_angle = student.mode_attention_angle
    student.attention_angle_per_frame = [x/mode_attention_angle for x in attention_list]
    


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
        box = extend_box(top_left, bottom_right, 50)
        
        
        for student in student_list:
            img = next_frame.copy()
            test_top_left = student.face_points['left_eye']
            test_bottom_right = student.face_points['mouth_right']
            
            # cv2.circle(img, test_top_left,1,(0,0,255),2)
            # cv2.circle(img, test_bottom_right,1,(0,0,255),2)
            # cv2.rectangle(img, extended_top_left, extended_bottom_right, (255,255,0),1)
            # show_image(img)

            if point_in_box(box, test_top_left) and point_in_box(box, test_bottom_right):
                found = True
                #print("found")
                break
            
            
        if found == False:
            #print("added student")
            max_name = max([int(x.name) + 1 for x in student_list])
            # attention = [len(x.attention_angle_list) for x in student_list]
            # max_attention = max(attention)
            # print(attention)
            # TODO: instead of zero add noise
            attention_list = [0 for i in range(index + 1)]
            student_list.append(Student(face,max_name))
            student_list[-1].attention_angle_list = attention_list
        

def check_for_absent(student_list):
    """checks if student is missing for 10 frames and removes them

    Args:
       student_list: list of students

    Returns:
        list of students

    """
    i = 0
    for student in student_list:
        if student.absent_from_frame >= 10:
            student_list.pop(i)
            # print("removed student")
        i += 1


def student_attentiveness():
    """gets the student attentiveness for the lecture

    Returns:
        a csv of attentiveness

    """
    if os.name == 'posix':
        delimiter = '/'
    else:
        delimiter = '\\'

    current_directory = os.getcwd()
    data_directory = os.path.abspath(os.path.join(current_directory, os.pardir + delimiter + 'data'))
    screenshot_directory = os.path.abspath(os.path.join(data_directory + delimiter + 'screenshot'))
    list_of_files = sorted(os.listdir(screenshot_directory))

    for i in range(len(list_of_files)):
        img = cv2.imread(screenshot_directory + delimiter + list_of_files[i])
        # print(screenshot_directory + delimiter + list_of_files[i])
        if i == 0:
            student_list = initial_frame(img)
        for student in student_list:
            try:
                next_frame = cv2.imread(screenshot_directory + delimiter + list_of_files[i+1])
                find_student_next_frame(student, next_frame)
            except IndexError:
                break
        find_new_students(student_list, next_frame, i + 1)
        check_for_absent(student_list)
    classroom_angles = []         
    for student in student_list:
        get_mode_angle(student)
        get_attention_per_frame(student)
        classroom_angles.append(student.attention_angle_per_frame)

    avg_across_lecture = np.mean(classroom_angles,axis=0)
    np.savetxt(data_directory + delimiter + 'attentiveness.csv', avg_across_lecture, delimiter=',', header='attentiveness')

    #return classroom_angles
    return student_list


if __name__ == '__main__':
    from split_video import split
    from analyze_video import screencap_video
    import time
    start_time = time.time()
    
    lecture = 'class1facingstudents.mov'
    split(lecture, 'students')
    screencap_file = 'students-output-video.mp4'
    screencap_video(screencap_file)
    student_list = student_attentiveness()
    print(time.time() - start_time)
    # 2038.2424449920654
