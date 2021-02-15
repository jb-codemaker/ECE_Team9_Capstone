import os
import sys

# TODO: allow spaces in path
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

    if os.path.exists(data_directory + delimiter + perspective + '-output-audio.mp4'):
        os.remove(data_directory + delimiter + perspective + '-output-audio.mp4')

    if os.path.exists(data_directory + delimiter + perspective + '-output-video.mp4'):
        os.remove(data_directory + delimiter + perspective + '-output-video.mp4')

    os.system('ffmpeg -i '+ '"' + parent_file + '"' + ' -vn -acodec copy '+ '"' + data_directory + delimiter + perspective + '-output-audio.mp4'  + '"' + ' -hide_banner -loglevel error')
    os.system('ffmpeg -i '+ '"' + parent_file  + '"' +' -c copy -an '+ '"' + data_directory + delimiter + perspective + '-output-video.mp4'  + '"' + ' -hide_banner -loglevel error')

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("\nFile and Perspective 1 or 2 is needed")
        sys.exit()
    file_name = sys.argv[1]
    perspective = sys.argv[2]
    split(file_name, perspective)
    print("\nSplit function complete\n")