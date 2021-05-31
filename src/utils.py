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

def get_duration(path):
    """gets length of video

    Args:
       path: path to lecture

    Returns:
        datetime obj of duration

    """
    duration_command = ['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1', "-sexagesimal", path, "-hide_banner"]

    duration_proc = duration_proc = subprocess.run(duration_command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    duration_str = str(duration_proc.stdout)[2:-3]
    
    duration = datetime.datetime.strptime(duration_str, '%H:%M:%S.%f')

    return duration

def get_frame(path, current_time):
    """takes a screen shot of a video and saves it in data/dir

    Args:
       file_name: output-video.mp4
       current_time: frame to capture
    
    
    Returns:
        nparray of frame

    """
    ffmpeg_command = ["ffmpeg", "-i", path, "-ss", str(current_time.time()), "-vframes","1", "-c:v", "png", "-f", "image2pipe", "pipe:1", '-hide_banner']
    pipe = subprocess.run(ffmpeg_command,
                          stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE)
    print(pipe.stdout)
    matrix = np.asarray(bytearray(pipe.stdout),dtype=np.uint8)
    # sys.stdout.flush()
    return matrix    

if __name__ == '__main__':
    import time
    current_time = datetime.datetime.strptime('00:00:00.000', '%H:%M:%S.%f')
    file_path = get_path("class1facingstudents.mov")
    
    duration = get_duration(file_path)
    resolution = 10
    start_time = time.time()
    print(duration)
    while current_time <= duration:
        print(current_time.time())
        frame = get_frame(file_path, current_time)
        img_cv = cv2.imdecode(frame, cv2.IMREAD_ANYCOLOR)
        # show_image(img_cv)
        current_time = current_time + datetime.timedelta(seconds=resolution)
    print(time.time() - start_time)

