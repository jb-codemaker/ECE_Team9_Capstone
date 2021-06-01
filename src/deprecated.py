import datetime
import numpy as np
import cv2
from utils import get_path
"""
these are functions that are no longer necesary
"""
def find_rectangle(contour):
    """finds rectangular contours
    
    Args:
       contour: the contour we are working on
    
    Returns:
       rectangle contour
    
    """
    arc = cv2.arcLength(contour, True)
    sides = cv2.approxPolyDP(contour, 0.02 * arc, True)

    return len(sides) == 4

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
    """This function is really cool, Instead of saving the frame locally it pipes the output to stdout, and then the frame can be read to memory! its really really slow though. such a shame

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
