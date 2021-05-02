import os
import sys
import shutil

# All this program does is take a screenshot every ten seconds
## needs to be run after splitdata

def screencap_video(file_path):
    """takes a screen shot of a video and saves it in data/dir

    Args:
       file_path: output-video.mp4


    """
    
    #specifies delimiter
    if os.name == 'posix':
        delimiter = '/'
    else: 
        delimiter = '\\'
    
    current_directory = os.getcwd()
    data_directory = os.path.abspath(os.path.join(current_directory, os.pardir + delimiter + 'data'))
    screenshot_directory = os.path.abspath(os.path.join(data_directory + delimiter + 'screenshot'))
    
    if os.path.isdir(screenshot_directory):
        shutil.rmtree(screenshot_directory)
        os.mkdir(screenshot_directory)
    else:
        os.mkdir(screenshot_directory)
        
    os.chdir(screenshot_directory)
    os.system('ffmpeg -i '+ file_path +' -vf fps=1/10 screenshot-%03d.png -hide_banner -loglevel error')
    os.chdir(current_directory)

if __name__ == '__main__':
    
    file_path = "/home/leo/Projects/ECE_Team9_Capstone/data/output.mp4"
    screencap_video(file_path)
