import cv2
import subprocess
import numpy
import datetime
import cv2
import numpy as np
import os
import sys

def show_image(img, annotation="image"):
    """quickly show image for debugging

    Args:
       img: img to view
       annotation: more definition


    """
    cv2.imshow(str(annotation), img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def extend_box(top_left, bottom_right, dx):
    """gets a box from a face in order to crop image to look for face again

    Args:
       top_left:     point for top left
       bottom_right: point for bottom_right
       dx:           the new box size

    Returns:


    """
    top_left = (top_left[0] - dx, top_left[1] - dx)
    bottom_right = ((bottom_right[0] + dx, bottom_right[1] + dx))
    return (top_left, bottom_right)


def point_in_box(box, test_point):
    """checks if a point is in a box

    Args:
       box: two points, a top left and a bottom right
       test_point: a test point

    Returns:
        bool

    """
    top_left = box[0]
    bottom_right = box[1]

    if (top_left[0] < test_point[0]) and (top_left[1] < test_point[1]) \
       and (bottom_right[0] > test_point[0]) and (bottom_right[1] > test_point[1]):
        return True
    else:
        return False

   
def get_data_dir():
    """

    Returns:
        path to data_dir

    """
    delimiter = get_delimiter()
    current_directory = os.getcwd()
    data_directory = os.path.abspath(os.path.join(current_directory, os.pardir + delimiter + 'data'))
   
    data_directory = data_directory.replace(' ', '\ ')

    return data_directory
    
def get_path(file_name):
    """gets the path to file from data_directory

    Args:
       file: file to find

    Returns:
        full path of file

    """
    
    data_directory = get_data_dir()
    delimiter = get_delimiter()
    
    path = data_directory + delimiter + file_name

    return path

def get_delimiter():
    """finds path delimiter

    Returns:
        delimiter

    """
    if os.name == 'posix':
        delimiter = '/'
    else: 
        delimiter = '\\'
    return delimiter


def get_screenshot_dir():
    """returns screenshot directory

    Returns:
        screenshot directory

    """
    delimiter = get_delimiter()
    data_dir = get_data_dir()
    screenshot_dir = data_dir + delimiter + 'screenshot'

    return screenshot_dir


