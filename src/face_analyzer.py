import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '1'
import tensorflow as tf
import cv2
from mtcnn import MTCNN
import numpy as np
import math
import random
import utils
import logging


logging.getLogger('tensorflow').disabled = True

config = tf.compat.v1.ConfigProto()
config.gpu_options.allow_growth = True
session = tf.compat.v1.Session(config=config)

print("Num GPUs Available: ", len(tf.config.list_physical_devices('GPU')))
# tf.debugging.set_log_device_placement(True)

class Student:
    
    def __init__(self, face, name):
        self.face = face
        self.name = name
        self.box = face['box']
        self.face_points = face['keypoints']
        self.attention_points = (0,0)
        self.reference_points = (0,0)
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
    # utils.show_image(im)
    student.attention_points = ((int(image_points[0][0]), int(image_points[0][1])), (int(nose_end_point2D[0][0][0]), int(nose_end_point2D[0][0][1])))

    # make a reference line
    vect = make_vect(student.attention_points[0],student.attention_points[1])
    
    d = get_magnitude(vect)

    student.reference_points = ((int(image_points[0][0]), int(image_points[0][1])), (int(image_points[0][0] + d), int(image_points[0][1])))
    
    # cv2.line(im,student.attention_points[0],student.attention_points[1], (255,0,0), 2)
    # cv2.line(im, student.reference_points[0],student.reference_points[1],(0,255,0),2)
    # utils.show_image(im)
    

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
    
    student_box = utils.extend_box(top_left_point, bottom_right_point, 50)
    
    mask = np.zeros(next_image.shape[:2], dtype=np.uint8)
    mask[student_box[0][1]:student_box[1][1]+1,student_box[0][0]:student_box[1][0]+1] = 255
    rect_img = cv2.bitwise_and(next_image,next_image,mask=mask)
    
    face = find_faces(rect_img)
    if len(face) > 1:
        # TODO(#17): find a way to decrease dx and call function again
        # print("more faces")
        
        student.attention_angle_list.append(random.randint(1,359))
    if len(face) < 1:
        #if no face append with noise
        #print("no face")
        student.attention_angle_list.append(random.randint(1,359))
        student.absent_from_frame += 1
            
    if len(face) == 1:
        student.update_face = face[0]
        get_pose_direction(student,next_image)
        get_angle(student)
        student.absent_from_frame = 0

    # utils.show_image(rect_img)
    # return student


def make_vect(point1,point2):
    """makes a vector out of 2 points

    Args:
       point1: first point
       point2: second point

    Returns:
        vector of 2 points (tuple)

    """
    
    return ((point2[0] - point1[0]),(point2[1] - point1[1]))

def get_magnitude(vector):
    """gets the magnitude of a vector

    Args:
       vector: vector to get a magnitude (tuple)

    Returns:
        the magnitude of a vector

    """
    return np.sqrt((vector[0])**2 + (vector[1])**2)

def get_angle(student):
    """gets the angle of the slope of the points (best we could do), appends that angle to angle list


    Args:
       student: thestudent working on
    """
    # NOTE: a bit over engineered but its sunday :)
    # turn attention_points and reference_points into vectors
    attention_points = student.attention_points
    reference_points = student.reference_points
    
    attention_vec = make_vect(attention_points[0], attention_points[1])

    reference_vec = make_vect(reference_points[0], reference_points[1])
    # print(attention_points)
    # print(attention_vec)

    # get angle between those vectors
    ## get magnitude of two vectors
    attention_mag = get_magnitude(attention_vec)
    reference_mag = get_magnitude(reference_vec)

    ## dot product
    dot_product = lambda a, b: (a[0] * b[0]) + (a[1] * b[1])

    attention_reference_dot = dot_product(attention_vec, reference_vec)
    # print("attention reference dot " + str(attention_reference_dot))
    # print("attention magnitude " + str(attention_mag))
    # print("reference magnitude " + str(reference_mag))
    
    angle = int(math.degrees(math.acos(attention_reference_dot/(attention_mag*reference_mag))))
    # append angle
    student.attention_angle_list.append(angle)
    # print("\n")
    # print("angle " + str(angle))
    # print("\n")
    
def get_mode_angle(student):
    """gets the mode angle (students are assumed to be paying attention most of the time)

    Args:
       student: student object


    """
    angle_list = student.attention_angle_list

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

    attention_angle_per_frame_raw = [abs((x - mode_attention_angle)/mode_attention_angle) for x in attention_list]

    # little hackey but mapping extreme high error to 0.00001
    attention_angle_per_frame = []
    for i in attention_angle_per_frame_raw:
        if i > 1.0:
            attention_angle_per_frame.append(.000001)
        else:
            attention_angle_per_frame.append(1 - i)
    

    student.attention_angle_per_frame = attention_angle_per_frame
    


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
            img = next_frame.copy()
            test_top_left = student.face_points['left_eye']
            test_bottom_right = student.face_points['mouth_right']
            
            # cv2.circle(img, test_top_left,1,(0,0,255),2)
            # cv2.circle(img, test_bottom_right,1,(0,0,255),2)
            # cv2.rectangle(img, extended_top_left, extended_bottom_right, (255,255,0),1)
            # utils.show_image(img)

            if utils.point_in_box(box, test_top_left) and utils.point_in_box(box, test_bottom_right):
                found = True
                #print("found")
                break
            
            
        if found == False:
            #print("added student")
            max_name = max([int(x.name) + 1 for x in student_list])
            attention_list = [random.randint(1,359) for i in range(index + 1)]
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
    delimiter = utils.get_delimiter()
    data_directory = utils.get_data_dir()
    screenshot_directory = utils.get_screenshot_dir()
    student_directory = screenshot_directory + "/students"

    list_of_files = sorted(os.listdir(student_directory))

    for i in range(len(list_of_files)):
        img = cv2.imread(student_directory + delimiter + list_of_files[i])
        # print(student_directory + delimiter + list_of_files[i])
        if i == 0:
            student_list = initial_frame(img)
        for student in student_list:
            try:
                next_frame = cv2.imread(student_directory + delimiter + list_of_files[i+1])
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

    return student_list


if __name__ == '__main__':
    from split_video import split
    import time
    
    start_time = time.time()
    
    lecture = 'class1facingstudents.mov'
    file_path = os.path.join(utils.get_data_dir(),lecture)
    split(file_path, 'students')
    student_list = student_attentiveness()
    print(time.time() - start_time)
