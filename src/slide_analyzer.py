import os
import cv2
import numpy as np
import utils
from classes import Slide
import img_funcs

debug = False
if debug:
    sharp = 0
    delimiter = utils.get_delimiter()
    debug_dir = utils.get_screenshot_dir() + delimiter + 'debug' + delimiter + 'slide_analyzer'
    if not os.path.exists(debug_dir):
        os.makedirs(debug_dir)


def analyze_lecture():
    """analyzes slides in lecture
   
    Returns:
        slide_list: a list of slide objects

    """
    delimiter = utils.get_delimiter()
    
    slide_directory = utils.get_screenshot_dir() + delimiter + "teacher"
    
    list_of_files = sorted(os.listdir(slide_directory))
    
    slide_list = []
    for i in range(len(list_of_files)):
        # print(slide_directory + delimiter + list_of_files[i])
        img = cv2.imread(slide_directory + delimiter + list_of_files[i])
        # utils.show_image(img)
        slide = img_funcs.find_slide(img)
        
        global debug
        if debug:
            global sharp
            global delimite
            global debug_dir
            cv2.imwrite(debug_dir + delimiter + 'slide_found-' + str(sharp) + '.jpg', slide)
            sharp += 1
            
        # initialize slide
        if i == 0:
            slide_list.append(Slide(slide, i + 1))
            previous_slide = slide
            # check if slide in next frame is the same
        else:
            if check_if_same_slide(previous_slide, slide):
                slide_list.append(slide_list[i-1])
            else:
                slide_list.append(Slide(slide, slide_list[i-1].name + 1))
        previous_slide = slide
    
    word_count_and_name = [[int(x.word_count), int(x.name)] for x in slide_list]
    total_slides = len(set([x.name for x in slide_list]))
    
    delimiter = utils.get_delimiter()
    data_directory = utils.get_data_dir()
    
    with open(data_directory + delimiter + 'total_slides.txt','w') as f:
        f.write(str(total_slides))
    
    np.savetxt(data_directory + delimiter + 'slide.csv', word_count_and_name, delimiter=',', fmt='%d', header='word_count,name')
    return slide_list


# check if current slide is the same as last slide
def check_if_same_slide(previous_slide, current_slide):
    """the object has the previous slide and the img is the current slide. if the two are the same update the object

    Args:
       previous_slide: slide: slide object
       next_slide:  image to check
    
    
    """
    # utils.show_image(current_slide, "current slide")
    # utils.show_image(next_slide, "next slide")
    height, width = current_slide.shape[:2]
    
    next_perspective = img_funcs.fix_perspective(previous_slide, height, width)
    # utils.show_image(current_slide, "current slide")
    # utils.show_image(next_perspective, "next")
    
    return img_funcs.image_similarity(current_slide, next_perspective)


if __name__ == '__main__':
    ###### IMPORTANT #########
    # youtube-dl https://www.youtube.com/watch?v=mwxknB4SgvM&t=792s #
    # move into data directory and name it Constraints_and_Hallucinations.mp4 #
    import split_video
    import time
    start_time = time.time()
    #lecture = "Constraints_and_Hallucinations.mp4"
    #file_path = os.path.join(utils.get_data_dir(), lecture)
    #split_video.split(file_path, "teacher")
    slide_list = analyze_lecture()
    print(time.time() - start_time)
    # text = [x.text for x in slide_list]
