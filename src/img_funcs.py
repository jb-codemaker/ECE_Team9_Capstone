import cv2
import numpy as np
from contours import corners_in_contour, get_outer_corners

def make_border(img):
    """makes an image with a border

    Args:
       img: image

    Returns:
       image with border

    """
    row, col = img.shape[:2]

    # add border to image in case slide is at edge
    border_size = 10
    img = cv2.copyMakeBorder(
        img,
        top=border_size,
        bottom=border_size,
        left=border_size,
        right=border_size,
        borderType=cv2.BORDER_CONSTANT,
        value=[0, 0, 0]
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
    blur = cv2.GaussianBlur(gray, (33, 33), 0)
    thresh = cv2.threshold(blur, 127, 225, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
    
    corners = find_corners(img)
    
    cnts, heirarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    heirarchy = heirarchy[0]
    # get largest contour that isnt the big one
    inner_cnts = []
    for i in range(len(cnts)):
        if (heirarchy[i][3] != -1):
            if corners_in_contour(cnts[i], corners):
                # x,y,w,h = cv2.boundingRect(cnts[i])
                # cv2.rectangle(img,(x, y), (x+w, y+h), (0, 255, 0),2)
                # utils.show_image(img)
                inner_cnts.append(cnts[i])
    
    # TODO(#19): edit out teacher
        
    try:
        max_contour = max(inner_cnts, key=cv2.contourArea)
        x,y,w,h = cv2.boundingRect(max_contour)
        crop = img[y:y+h, x:x+w]
        height, width = crop.shape[:2]
        slide = fix_perspective(crop, height, width)
        # utils.show_image(crop, "crop")
        # utils.show_image(slide, "fixed perspective")
        kernel = np.array([[-1, -1, -1],
                           [-1, 9, -1],
                           [-1, -1, -1]])
        sharpend = cv2.filter2D(slide, -1, kernel)
        # utils.show_image(sharpend)
        return sharpend
        
    except ValueError:
        return img


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
    corners = cv2.cornerSubPix(gray, np.float32(centroids), (5, 5), (-1, -1), criteria)
    # img[dst>0.01*dst.max()]=[0,0,255]
    return corners

def image_similarity(image1, image2):
    """checks similarity between two images by cross correlation and sees if the pixels are the same

    Args:
       image1: image 1
       image2: image 2

    Returns:
        boolian: if slide is same true
    
    """
    ones = np.ones((55, 55)) 
    scalar = ones.shape[0] ** 2
    kernel = ones / scalar
    
    img1 = convolve_image(image1, kernel)
    img2 = convolve_image(image2, kernel)
    # utils.show_image(image1, "image1")
    # utils.show_image(image2, "image2")
    
    error = compare_image(img1, img2)

    threshold = 3
    if error <= threshold:
        return True
    else:
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

    return np.dstack([convolve(image[:, :, z], kernel, stride=kernel.shape[0]) for z in range(3)]).astype('uint8')


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


def fix_perspective(image, height, width):
    """changes the perspective of the image

    Args:
       image: image to warp
       height: height to warp to
       width: widht to warp to

    Returns:
        image with changed perspective

    """
    image_border = make_border(image)
    corners = find_corners(image_border)
    normalized_corners = np.float32([[0, 0], [width, 0], [0, height], [width, height]])
    outer_corners = np.float32(get_outer_corners(corners))
    matrix = cv2.getPerspectiveTransform(outer_corners, normalized_corners)
    perspective = cv2.warpPerspective(image_border, matrix, (width, height))
    # utils.show_image(perspective)
    return perspective
