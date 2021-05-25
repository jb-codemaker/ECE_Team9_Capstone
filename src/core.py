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
import split_video      # Splits .mp4 file

from visualize_data import visualize

def main():

    # Take args and split video/audio into seperate files
    if len(sys.argv) < 3:
        print("\nFile and Perspective 1 or 2 is needed")
        sys.exit()
    file_name = sys.argv[1]
    perspective = sys.argv[2]
    split_video.split(file_name, perspective)
    print("\nSplit function complete\n")

    # TODO(#23): Clone https://github.com/tyiannak/pyAudioAnalysis.git
    #       Audio analysis tool

    # TODO: Clone https://github.com/tyiannak/pyAudioAnalysis.git
    #       Audio analysis tool

    if __name__ == '__main__':
        #split the data

        #send video to video analyzer

        #send audio to audio analyzer

        #split slide data

        #send slide data to slide analyzer

        #visualize it
        visualize(r"ECE_Team9_Capstone\data\Sample_csv.csv")
