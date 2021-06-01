import numpy as np

def make_vect(point1,point2):
    """makes a vector out of 2 points

    Args:
       point1: first point
       point2: second point

    Returns:
        vector of 2 points (tuple)

    """
    
    return ((point2[0] - point1[0]),(point2[1] - point1[1]))

def get_magnitude(vector):
    """gets the magnitude of a vector

    Args:
       vector: vector to get a magnitude (tuple)

    Returns:
        the magnitude of a vector

    """
    return np.sqrt((vector[0])**2 + (vector[1])**2)
