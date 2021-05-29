# Project: An Algorithmic Teaching Practices and Classroom Activities Tool to Improve Education
#
# Authors: Joshua Blazek, Leo Garcia, Naiqi Yao, and Jinghan Zhang
#
# Sponsor: Christof Teuscher and teuscher-lab.com
#
# Ownership: See https://github.com/jb-codemaker/ECE_Team9_Capstone for license details
#
#
# This file: Splits a video/audio file into seperate files.

import os
import sys
import utils
import shutil

def split(file_name, perspective):
    """Takes a movie file and saves to two mp4 files. One is video only, the other one is audio only.

    ARGS:
        file_name: video file
        perspective: either students or teacher

        
    """

    current_directory = os.getcwd()
    delimiter = utils.get_delimiter()
    data_directory = utils.get_data_dir()
    screenshot_dir = utils.get_screenshot_dir()
    
    parent_file =  data_directory + delimiter + file_name
    
    if os.path.exists(data_directory + delimiter + perspective + '-output-audio.wav'):
        os.remove(data_directory + delimiter + perspective + '-output-audio.wav')

    ###### DO NOT MESS WITH THIS ######
    if os.path.exists(screenshot_dir + delimiter + perspective):
        shutil.rmtree(screenshot_dir + delimiter + perspective)
    ###################################
    
    if not os.path.exists(screenshot_dir + delimiter + perspective):
        os.mkdir(screenshot_dir + delimiter + perspective)
    
    os.system('ffmpeg -i '+ '"' + parent_file + '"' + ' -vn -acodec pcm_s16le -ar 44100 -ac 2 '+ '"' + data_directory + delimiter + perspective + '-output-audio.wav'  + '"' + ' -hide_banner -loglevel error')
    os.system("ffmpeg -i " + parent_file + " -vf fps=1/10 " + screenshot_dir + delimiter + perspective+delimiter + "image.%04d.jpg -hide_banner -loglevel error")

    return perspective

if __name__ == '__main__':
    split('class1facingstudents.mov','students')
    
    '''
    if len(sys.argv) < 3:
        print("\nFile and Perspective 1 or 2 is needed")
        sys.exit()
    file_name = sys.argv[1]
    perspective = sys.argv[2]
    split(file_name, perspective)

    print("\nSplit function complete\n")
    '''
