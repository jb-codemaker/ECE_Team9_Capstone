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

def split(file_name, perspective):
    """Takes a movie file and saves to two mp4 files. One is video only, the other one is audio only.

    ARGS:
        file_name: video file
        perspective: either students or teacher

        
    """
    if os.name == 'posix':
        delimiter = '/'
    else: 
        delimiter = '\\'

    current_directory = os.getcwd()
    data_directory = os.path.abspath(os.path.join(current_directory, os.pardir + delimiter + 'data'))

    parent_file =  data_directory + delimiter + file_name

    if os.path.exists(data_directory + delimiter + perspective + '-output-audio.wav'):
        os.remove(data_directory + delimiter + perspective + '-output-audio.wav')

    if os.path.exists(data_directory + delimiter + perspective + '-output-video.mp4'):
        os.remove(data_directory + delimiter + perspective + '-output-video.mp4')

    os.system('ffmpeg -i '+ '"' + parent_file + '"' + ' -vn -acodec pcm_s16le -ar 44100 -ac 2 '+ '"' + data_directory + delimiter + perspective + '-output-audio.wav'  + '"' + ' -hide_banner -loglevel error')
    os.system('ffmpeg -i '+ '"' + parent_file  + '"' +' -c copy -an '+ '"' + data_directory + delimiter + perspective + '-output-video.mp4'  + '"' + ' -hide_banner -loglevel error')

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("\nFile and Perspective 1 or 2 is needed")
        sys.exit()
    file_name = sys.argv[1]
    perspective = sys.argv[2]
    split(file_name, perspective)

    print("\nSplit function complete\n")
