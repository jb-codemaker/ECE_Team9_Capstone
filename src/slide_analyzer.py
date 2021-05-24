import os
import cv2
import numpy as np
from functools import reduce
import operator
from utils import show_image, extend_box, point_in_box

class Slide:
    def __init__(self, slide, name):
        "slide object has cropped img of slide"
        self.slide = slide #img
        self.name = name
        

# iterate through files
def analyze_lecture():
    """iterates through screenshoted lecture
    
    Returns:
        IDK
    """
    if os.name == 'posix':
        delimiter = '/'
    else:
        delimiter = '\\'
    
    current_directory = os.getcwd()
    data_directory = os.path.abspath(os.path.join(current_directory, os.pardir + delimiter + 'data'))
    screenshot_directory = os.path.abspath(os.path.join(data_directory + delimiter + 'screenshot'))
    
    list_of_files = sorted(os.listdir(screenshot_directory))

    slide_list = []
    for i in range(len(list_of_files)):
        img = cv2.imread(screenshot_directory + delimiter + list_of_files[i])
        # initialize slide
        if i == 0:
            slide = find_slide(img)
            slide_list.append(Slide(slide, i))
        # check if slide in next frame is the same
        try:
            next_img = cv2.imread(screenshot_directory + delimiter + list_of_files[i + 1])
            # show_image(next_img, str(i))
            next_slide = find_slide(next_img)
            slide_list.append(Slide(next_slide,i+1))

            
            test = check_if_same_slide(slide_list[i], next_slide)
            if i+1 == 15:
                break
        except IndexError:
            pass
    return slide_list

def find_rectangle(contour):
    """finds rectangular contours
    
    Args:
       contour: the contour we are working on
    
    Returns:
       rectangle contour
    
    """
    arc = cv2.arcLength(contour, True)
    sides = cv2.approxPolyDP(contour, 0.02 * arc, True)
    #print(approximation)

    return len(sides) == 4

def make_border(img):
    """makes an image with a border

    Args:
       img: image

    Returns:
       image with border

    """
    row, col = img.shape[:2]
    bottom = img[row-2:row, 0:col]
    mean = cv2.mean(bottom)[0]

    # add border to image in case slide is at edge
    border_size = 10
    img = cv2.copyMakeBorder(
        img,
        top = border_size,
        bottom = border_size,
        left = border_size,
        right = border_size,
        borderType = cv2.BORDER_CONSTANT,
        value = [mean,mean,mean]
    )
    return img


def find_slide(img):
    """finds the slide in an image

    Args:
       img: image to find slide in

    Returns:
        cropped slide if found

    """
    img = make_border(img)
    
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (33,33), 0)
    thresh = cv2.threshold(blur, 127, 225, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
    
    corners = find_corners(img)
    
    cnts, heirarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    heirarchy = heirarchy[0]
    # get largest contour that isnt the big one
    inner_cnts = []
    for i in range(len(cnts)):
        found_slide = False
        if (heirarchy[i][3] != -1):
            if corners_in_contour(cnts[i],corners):
            # if find_rectangle(cnts[i]):
                # x,y,w,h = cv2.boundingRect(cnts[i])
                # cv2.rectangle(img,(x, y), (x+w, y+h), (0, 255, 0),2)
                # show_image(img)
                found_slide = True
                inner_cnts.append(cnts[i])
    
    # TODO(#19): edit out teacher
        

    try:
        slide = max(inner_cnts, key=cv2.contourArea)
        x,y,w,h = cv2.boundingRect(slide)
        crop = img[y:y+h, x:x+w]
        # change perspective so that the image right on (maybe important maybe not)
        # show_image(crop)
        return crop
        
    # TODO(#21): firgure out a better thing to return if no slide
    except ValueError:
        return np.nan

def corners_in_contour(contour, corners):
    """finds if there are 4 or more corners in a contour

    Args:
       contour: current contour
       corners: corners to test

    Returns:
        bool

    """
    corner_found = 0
    x,y,w,h = cv2.boundingRect(contour)
    box = extend_box((x,y), (x+w,y+h), 5)
    
    for corner in corners:
        if point_in_box(box, corner):
            corner_found += 1
        if corner_found >= 4:
            return True

    return False

def find_corners(img):
    """finds the corners of the image

    Args:
       img: img to find corners

    Returns:
        corners of the image

    """
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = np.float32(gray)
    dst = cv2.cornerHarris(gray, 9, 7, 0.04)
    ret, dst = cv2.threshold(dst, 0.1 * dst.max(), 255, 0)
    dst = np.uint8(dst)
    ret, labels, stats, centroids = cv2.connectedComponentsWithStats(dst)
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.001)
    corners = cv2.cornerSubPix(gray,np.float32(centroids),(5,5),(-1,-1),criteria)
    # img[dst>0.01*dst.max()]=[0,0,255]
    return corners

# check if current slide is the same as last slide
# corrilation matrix
def check_if_same_slide(slide_obj, next_slide):
    """the object has the previous slide and the img is the current slide. if the two are the same update the object

    Args:
       slide_obj: slide object
       next_slide:  image to check
    
    
    """
    current_slide = make_border(slide_obj.slide)
    current_corners = find_corners(current_slide)
    height, width = current_slide.shape[:2]

    normalized_corners = np.float32([[0,0], [width,0], [0,height], [width,height]])
    outer_current_corners = np.float32(get_outer_corners(current_corners))

    # for corner in outer_current_corners:
    #     x,y = corner[0], corner[1]
    #     cv2.circle(current_slide, (x,y), 1, (0,0,255),3)
    # show_image(current_slide)
    
    current_matrix = cv2.getPerspectiveTransform(outer_current_corners, normalized_corners)
    current_perspective = cv2.warpPerspective(current_slide, current_matrix, (width, height))

    next_slide = make_border(next_slide)
    next_corners = find_corners(next_slide)

    outer_next_corners = np.float32(get_outer_corners(next_corners))

    next_matrix = cv2.getPerspectiveTransform(outer_next_corners, normalized_corners)
    next_perspective = cv2.warpPerspective(next_slide, next_matrix, (width, height))
    
    # show_image(current_perspective, "current")
    # show_image(next_perspective, "next")
    image_similarity(current_perspective,next_perspective)
    
    return True

def get_outer_corners(corners):
    """gets the outer box of corners

    Args:
       corners: list of corners to iterate

    Returns:
        4 of the outer corners

    """
    top_left = corners[0]
    top_right = corners[0]
    bottom_left = corners[0]
    bottom_right = corners[0]
    for corner in corners:
        if corner[0] < top_left[0] and corner[1] < top_left[1]:
            top_left = corner
        if corner[0] < bottom_left[0] and corner[1] > bottom_left[1]:
            bottom_left = corner
        if corner[0] > top_right[0] and corner[1] < top_right[1]:
            top_right = corner
        if corner[0] > bottom_right[0] and corner[1] > bottom_right[1]:
            bottom_right = corner
    
    return [top_left, top_right, bottom_left, bottom_right]

def image_similarity(image1, image2):
    """checks similarity between two images by cross correlation and sees if the pixels are the same

    Args:
       image1: image 1
       image2: image 2

    Returns:
        boolian: if slide is same true
    
    """
    
    ones = np.ones((55,55)) 
    scalar = ones.shape[0] ** 2
    kernel = ones / scalar
    
    img1 = convolve_image(image1, kernel)
    img2 = convolve_image(image2, kernel)
    
    #show_image(image1, "image1")
    #show_image(image2, "image2")
    error = compare_image(image1, image2)
    # print(error)
    
    if error <= 20:
        # print("same slide")
        return True
    else:
        # print("not same slide")
        return False
    

def convolve(image, kernel, stride=1):
    """convolve the image without padding 

    Args:
       image: the image
       kernel: kernel
       stride: how pixels it jumps

    Returns:
        convolved image

    """
    height, width = image.shape
    k = kernel.shape
    
    height_out = np.floor((height - k[0] - (k[0] - 1) / stride) / stride).astype(int) + 1
    width_out = np.floor((width - k[1] - (k[1] - 1) / stride) / stride).astype(int) + 1
    
    image_out = np.zeros((height_out, width_out))
    
    b = k[0] // 2, k[1] // 2

    x_center_b = b[0]
    y_center_b = b[1]

    for i in range(height_out):
        center_x = x_center_b + i * stride
        index_x = [center_x + l for l in range(-b[0], b[0] + 1)]
        for j in range(width_out):
            center_y = y_center_b + j * stride
            index_y = [center_y + l for l in range(-b[0], b[0] + 1)]

            sub_image = image[index_x, :][:, index_y]

            image_out[i][j] = np.sum(np.multiply(sub_image, kernel))
            
    return image_out

def convolve_image(image, kernel):
    """applies a filter to an image

    Args:
       image: image to have filter
       kernel: odd shaped kernels

    Returns:
        image after kernel

    """
    kernel = np.asarray(kernel)

    return np.dstack([convolve(image[:, :, z], kernel, stride = kernel.shape[0]) for z in range(3)]).astype('uint8')
# if slide is not same OCR slide (count words)

def compare_image(image1, image2):
    """compares two images by checking each pixel and seeing if they are similar

    Args:
       image1: image 1 
       image2: image 2

    Returns:
        mean absolute error of image

    """
    absolute_error = 0
    flat1 = [int(pixel) for row in image1 for col in row for pixel in col]
    flat2 = [int(pixel) for row in image2 for col in row for pixel in col]

    for a, b in zip(flat1, flat2):
        absolute_error += abs(a-b)
        
    mean_absolute_error = np.floor(absolute_error / len(flat1))
    
    return mean_absolute_error

if __name__ == '__main__':
    ###### IMPORTANT #########
    # youtube-dl https://www.youtube.com/watch?v=mwxknB4SgvM&t=792s #
    # move into data directory and name it Constraints_and_Hallucinations.mp4 #
   from analyze_video import screencap_video
   
   # screencap_video("Constraints_and_Hallucinations.mp4")
   slide_list = analyze_lecture()
   # img_list = [x.slide for x in slide_list]
   # list(map(show_image, img_list))
