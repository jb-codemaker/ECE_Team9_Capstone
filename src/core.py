# Project: An Algorithmic Teaching Practices and Classroom Activities Tool to Improve Education
#
# Authors: Joshua Blazek, Leo Garcia, Naiqi Yao, and Jinghan Zhang
#
# Sponsor: Christof Teuscher and teuscher-lab.com
#
# Ownership: See https://github.com/jb-codemaker/ECE_Team9_Capstone for license details
#
#
# This file: Takes in arguments and splits, models, analyses, visualizes, email.

import os
import sys
import ray
import split_video      # Splits .mp4 file
import audio_model      # Diarizes and counts 
import utils
import face_analyzer
import slide_analyzer
from visualize_data import visualize

def main():
    ray.init()
    # Take args and split video/audio into seperate files
    # if len(sys.argv) < 3:
    #     print("\nFile and Perspective 1 or 2 is needed")
    #     sys.exit()
        
    file_name_1 = "class1facingstudents.mov" #sys.argv[1]
    file_name_2 = "racket.mkv" #sys.argv[2]
    
    @ray.remote
    def split_student(file_name_1):
        """this is just for concurrency

        Args:
           file_name_1: file_name for students

        Returns:
           the split function for students
        """
        return split_video.split(file_name_1, "students")

    @ray.remote
    def split_teacher(file_name_2):
        """this is just for concurrency

        Args:
           file_name_2: file_name for teachers

        Returns:
           the split function for teachers
        """
        return split_video.split(file_name_2, "teacher")
    
    # start the process
    split_funcs = [split_student.remote(file_name_1),split_teacher.remote(file_name_2)]

    # block before next section
    [ray.get(x) for x in split_funcs]

    @ray.remote(num_gpus=1)
    def student_call():
        """this is just for concurrency

        Returns:
           the student attentiveness function
        """
        return face_analyzer.student_attentiveness()

    @ray.remote
    def slide_call():
        """this is just for concurrency

        Returns:
           the slide analyzer function
        """
        return slide_analyzer.analyze_lecture()

    @ray.remote
    def audio_call():
        """this is just for concurrency

        Returns:
           the audio analyzer function
        """
        return audio_model.audio_analyze()

    # start the process
    call_funcs = [student_call.remote(), slide_call.remote(), audio_call.remote()]

    # block before next section
    [ray.get(x) for x in call_funcs]
    ray.shutdown()

    # TODO(#23): Clone https://github.com/tyiannak/pyAudioAnalysis.git
    #       Audio analysis tool

    # TODO: Clone https://github.com/tyiannak/pyAudioAnalysis.git
    #       Audio analysis tool

if __name__ == '__main__':
    main()
    print("ALL DONE")
    # visualize(r"ECE_Team9_Capstone\data\Sample_csv.csv")
