import cv2


def show_image(img, annotation="image"):
    """quickly show image for debugging

    Args:
       img: img to view
       annotation: more definition


    """
    cv2.imshow(str(annotation), img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def extend_box(top_left, bottom_right, dx):
    """gets a box from a face in order to crop image to look for face again

    Args:
       top_left:     point for top left
       bottom_right: point for bottom_right
       dx:           the new box size

    Returns:


    """
    top_left = (top_left[0] - dx, top_left[1] - dx)
    bottom_right = ((bottom_right[0] + dx, bottom_right[1] + dx))
    return (top_left, bottom_right)


def point_in_box(box, test_point):
    """checks if a point is in a box

    Args:
       box: two points, a top left and a bottom right
       test_point: a test point

    Returns:
        bool

    """
    top_left = box[0]
    bottom_right = box[1]

    if (top_left[0] < test_point[0]) and (top_left[1] < test_point[1]) \
       and (bottom_right[0] > test_point[0]) and (bottom_right[1] > test_point[1]):
        return True
    else:
        return False
