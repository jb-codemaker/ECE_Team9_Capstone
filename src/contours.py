import cv2
import utils


def corners_in_contour(contour, corners):
    """finds if there are 4 or more corners in a contour

    Args:
       contour: current contour
       corners: corners to test

    Returns:
        bool

    """
    corner_found = 0
    x, y, w, h = cv2.boundingRect(contour)
    box = utils.extend_box((x, y), (x+w, y+h), 5)

    for corner in corners:
        if utils.point_in_box(box, corner):
            corner_found += 1
        if corner_found >= 4:
            return True

    return False


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
