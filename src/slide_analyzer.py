import os
import cv2

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

    count = 0
    for i in range(len(list_of_files)):
        img = cv2.imread(screenshot_directory + delimiter + list_of_files[i])
        if find_slide(img):
            count +=1
       
    print(count/len(list_of_files)) #=> .74
        
def show_image(img, i = 0):
    """quickly show image for debugging

    Args:
       img: img to view


    """
    cv2.imshow("find_slide"+str(i), img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

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

    return not len(sides) != 4

def find_slide(img):
    """finds the slide in an image

    Args:
       img: image to find slide in

    Returns:
        cropped slide if found

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

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (55,55), 0)
    thresh = cv2.threshold(blur, 127, 225, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

    #show_image(thresh)
    
    cnts, heirarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    heirarchy = heirarchy[0]
    
    # get largest contour that isnt the big one
    inner_cnts = []
    for i in range(len(cnts)):
        if (heirarchy[i][3] != -1):
            if find_rectangle(cnts[i]):
                x,y,w,h = cv2.boundingRect(cnts[i])
                #cv2.rectangle(img,(x, y), (x+w, y+h), (0, 255, 0),2)
                inner_cnts.append(cnts[i])
            else:
                # usually if it cant find the rectangle the teacher is in the slide so figure a way to fix that
                # TODO(#19): edit out teacher
                pass



    try:
        slide = max(inner_cnts, key=cv2.contourArea)
        x,y,w,h = cv2.boundingRect(slide)
        crop = img[y:y+h, x:x+w]
        
        #show_image(crop,i)
        
        return True
        #return crop
        
    # TODO(#21): firgure out a better thing to return if no slide
    except ValueError:
        return False
        #return None


# check if current slide is the same as last slide
# corrilation matrix
def check_if_same_slide(slide_obj,img):
    """the object has the previous slide and the img is the current slide. if the two are the same update the object

    Args:
       slide_obj: slide object
       img: image to check


    """
    pass

# if slide is not same OCR slide (count words)

if __name__ == '__main__':
   from analyze_video import screencap_video


   #find_slide(img)

   analyze_lecture()
   
   #screencap_video("Constraints_and_Hallucinations.mp4")
