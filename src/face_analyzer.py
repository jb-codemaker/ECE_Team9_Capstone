import os
import cv2
import numpy as np
import utils
import student_img
import student_funcs


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
            student_list = student_img.initial_frame(img)
        for student in student_list:
            try:
                next_frame = cv2.imread(student_directory + delimiter + list_of_files[i+1])
                student_img.find_student_next_frame(student, next_frame)
            except IndexError:
                break
        student_img.find_new_students(student_list, next_frame, i + 1)
        student_funcs.check_for_absent(student_list)
    
    classroom_angles = []         
    for student in student_list:
        student_funcs.get_mode_angle(student)
        student_funcs.get_attention_per_frame(student)
        classroom_angles.append(student.attention_angle_per_frame)

    avg_across_lecture = np.mean(classroom_angles, axis=0)
    np.savetxt(data_directory + delimiter + 'attentiveness.csv', avg_across_lecture, delimiter=',', header='attentiveness')

    return student_list


if __name__ == '__main__':
    from split_video import split
    import time
    start_time = time.time()
    # lecture = 'class1facingstudents.mov'
    # file_path = os.path.join(utils.get_data_dir(),lecture)
    # split(file_path, 'students')
    student_list = student_attentiveness()
    print(time.time() - start_time)
