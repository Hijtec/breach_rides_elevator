"""A preprocessing module for button recognition.

#Assumptions:   TODO:

This module contains functions needed for preprocessing an image:
    grayscaling
    median filtering
    canny edge detection
    candidate ROI extraction
    size filtering

Typical usage example:
TODO:
"""
import cv2
import imutils
import numpy as np

def adjust_brightness_dynamic(image, brightness=0.0, contrast=0.0):
    out = imutils.adjust_brightness_contrast(image, brightness=brightness, contrast=contrast)
    return out

def grayscale(image):
    out = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return out

def median_filter(image, kernelsize=3):
    out = cv2.medianBlur(image, kernelsize)
    return out

def canny_edge_extraction(image, sigma=0.33, dilate_iterations=2, erode_iterations=1):
    edges = imutils.auto_canny(image, sigma)
    edges_dilated = cv2.dilate(edges, None, iterations=dilate_iterations)
    edges_eroded = cv2.erode(edges_dilated, None, iterations=erode_iterations)
    edges = edges_eroded
    return edges

def candidate_extraction(image, edges):
    cnts = cv2.findContours(edges, mode=cv2.RETR_EXTERNAL, method=cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    for (i, cnt) in enumerate(cnts):
        orig_label = contours.label_contour(image, cnt, i, color=[240, 0, 159])
    (cnts, boundingBoxes) = contours.sort_contours(cnts, method="bottom-to-top")
    clone = image.copy()
    for (i, cnt) in enumerate(cnts):
        sorted_label = contours.label_contour(clone, cnt, i, color=[240, 0, 159])

    return orig_label, sorted_label

def box_contours(image, contours):
    boxes = []
    for (i, cnt) in enumerate(contours[1]):
        rect = cv2.minAreaRect(cnt)
        box = cv2.boxPoints(rect)
        box = np.int0(box)
        boxes.append(box)
        image = cv2.drawContours(image,[box], 0, (0,0,255), 2)
    return image, boxes

def boxdimension_filter(image, boxes, size_lim = None, width_lim = None, height_lim = None, ratio_wh_lim = None):
    boxes_filtered = []
    for box in boxes:
        x1, y1 = box[0]
        x2, y2 = box[1]
        x3, y3 = box[2]
        x4, y4 = box[3]
        dx12 = abs(x1-x2)
        dy12 = abs(y1-y2)
        dx23 = abs(x2-x3)
        dy23 = abs(y2-y3)
        dy14 = abs(y1-y4)

        l12 = dx12 + dy12
        l23 = dx23 + dy23

        if dy12 <= dy14:
            width = l12
            height = l23
        else:
            width = l23
            height = l12

        size = l12 * l23
        #CRITERIA
        if size_lim != None:
            size_criteria = size >= size_lim[0] and size <= size_lim[1]
        else:
            size_criteria = True
        if height_lim != None:
            height_criteria = height >= height_lim[0] and height <= height_lim[1]
        else:
            height_criteria = True
        if width_lim != None:
            width_criteria = width >= width_lim[0] and width <= width_lim[1]
        else:
            width_criteria = True
        if ratio_criteria != None:
            ratio_criteria = width/height >= ratio_wh_lim[0] and width/height <= ratio_wh_lim[1]
        else:
            ratio_criteria = True
        #VALID BOX?
        if size_criteria and height_criteria and width_criteria and ratio_criteria:
            boxes_filtered.append(box)
        else:
            continue
    return boxes_filtered            

def draw_contours(image, contours, color):
    image = cv2.drawContours(image, contours, 0, (0,0,255), 2)
    return image

def show(name, frame):
    while True:
        cv2.imshow(name, frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break



