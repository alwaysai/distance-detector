import cv2 as cv
import edgeiq
from interest_item import InterestItem
import numpy as np
import math

def draw_distances(frame, KEY_ITEMS, KEY_PRED):
    """Calculates the distance between every object in KEY_PRED

    Args:
        frame (numpy array): The image
        KEY_ITEMS (list): a list of InterestItem objects
        KEY_PRED (list): Predictions for objects of interest

    Returns:
        tuple: The marked up frame and corresponding text
    """
    text = ""
    for key_pred in KEY_PRED:
        for item in KEY_ITEMS:
            if key_pred.label in item.labels:
                # calculate scale as pixels per inch
                pixel_scale = math.sqrt(key_pred.box.area)/math.sqrt(item.get_area())
        for other_pred in KEY_PRED:
            if key_pred is not other_pred:
                color = (66, 245, 93)
                # calculate distance in inches by dividing pixels by pixels per inch
                dist = key_pred.box.compute_distance(other_pred.box)/pixel_scale

                # draw the line between two objects of interest
                cv.line(frame, (int(key_pred.box.center[0]), int(key_pred.box.center[1])),
                                (int(other_pred.box.center[0]), int(other_pred.box.center[1])),
                                color, 6)
                if dist > 0.0:
                    text = "Items are {:.2f} in ({:.2f} cm) apart".format(dist, (dist * 2.54))
    return (frame, text)