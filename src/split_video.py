import os
import sys

# TODO: add perspective
def split(file_name):#, perspective):
    """takes a video and saves 2 files in the data directory, one being the audio file the other being the video file
    
    Args:
       file_name: file for the video
       perspective: either students or teacher
    
    
    """
    
    
    # TODO: test windows file systems
    current_directory = os.getcwd()
    data_directory = os.path.abspath(os.path.join(current_directory, os.pardir + "/data"))
    video_file = data_directory + "/" + file_name
    
    if os.path.exists(data_directory + "/output-audio.mp4"):
        os.remove(data_directory + "/output-audio.mp4")
        
    if os.path.exists(data_directory + "/output-video.mp4"):
        os.remove(data_directory + "/output-video.mp4")
        
    os.system("ffmpeg -i "+ video_file +" -vn -acodec copy "+ data_directory +"/output-audio.mp4 -hide_banner -loglevel error")
    os.system("ffmpeg -i "+ video_file +" -c copy -an "+ data_directory +"/output-video.mp4 -hide_banner -loglevel error")


if __name__ == '__main__':
    file_name = sys.argv[1]#"class1facingstudents.mov"
    split(file_name)
