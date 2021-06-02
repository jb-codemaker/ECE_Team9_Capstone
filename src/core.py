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


def main(file_name_1, file_name_2):
    ray.init()
    @ray.remote
    def split_student(file_path1):
        """this is just for concurrency

        Args:
           file_path1: file_path for students

        Returns:
           the split function for students
        """
        return split_video.split(file_path1, "students")

    @ray.remote
    def split_teacher(file_path2):
        """this is just for concurrency

        Args:
           file_path2: file_path for teachers

        Returns:
           the split function for teachers
        """
        return split_video.split(file_path2, "teacher")

    # start the process
    split_funcs = [split_student.remote(file_name_1), split_teacher.remote(file_name_2)]

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
    # Take args and split video/audio into seperate files
    if len(sys.argv) < 3:
        print("needs files for students: file_name_1, and teacher: file_name_2 \n python core.py \"path/to/class1facingstudents.mov\" \"path/to/teacher_lecture.mov\"")
        sys.exit()
    # data_dir = utils.get_data_dir()
    # teacher = os.path.join(data_dir, 'racket.mkv')
    # students = os.path.join(data_dir, 'class1facingstudents.mov')
    
    file_path1 = sys.argv[1]
    file_path2 = sys.argv[2]
    main(file_path1, file_path2)
    # visualize(r"ECE_Team9_Capstone\data\Sample_csv.csv")
    print("ALL DONE")
