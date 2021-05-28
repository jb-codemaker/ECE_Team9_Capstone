import os
import sys
import shutil

# All this program does is take a screenshot every ten seconds
## needs to be run after splitdata

def screencap_video(file_name):
    """takes a screen shot of a video and saves it in data/dir

    Args:
       file_name: output-video.mp4


    """
    
    #specifies delimiter
    if os.name == 'posix':
        delimiter = '/'
    else: 
        delimiter = '\\'
    
    current_directory = os.getcwd()
    data_directory = os.path.abspath(os.path.join(current_directory, os.pardir + delimiter + 'data'))
    screenshot_directory = os.path.abspath(os.path.join(data_directory + delimiter + 'screenshot'))

    file = data_directory + delimiter + file_name
    
    if os.path.isdir(screenshot_directory):
        shutil.rmtree(screenshot_directory)
        os.mkdir(screenshot_directory)
    else:
        os.mkdir(screenshot_directory)
        
    os.system('ffmpeg -i ' + '"' + file + '"' +' -vf fps=1/10 '+ '"' + screenshot_directory + delimiter + 'screenshot-%03d.png' + '"' + ' -hide_banner -loglevel error')

if __name__ == '__main__':
    
    file_name = "output.mp4"
    screencap_video(file_name)
