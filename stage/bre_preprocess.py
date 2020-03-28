"""A preprocessing module for button recognition.

#Input:         Camera Sensor output
#Output:        Panel ROI and Button ROIs
#Assumptions:   TODO:

This script utilises raw camera data and extracts relevant information
from it for further use. The principles used to process the data are:
    grayscaling
    median filtering
    canny edge detection
    candidate ROI extraction
    size filtering 

Typical usage example:
TODO:
"""
import imutils
import cv2
import numpy as np

class Image:
    """An object representing the data given.

    Attributes:
        id
        image
    
    Methods:
        aaa
        bbb
    
    Raises:
        jeden rejz
        druhy rejz
    """
    def __init__(self, id, image):
        """Initializes the class and calls its methods."""
        self.id = id
        self.image_raw = image
        self.image = image

class Preprocess:
    """An object representing the the preprocessing algorithm.

    Attributes:
        xxx
        yyy
    
    Methods:
        measure_perf:
        bbb
    
    Raises:
        jeden rejz
        druhy rejz
    """
    def __init__(self, id, image):
        """Initializes the class and calls its methods."""
        self.id = id
        self.tick_init = cv2.getTickCount()
        self.image_raw = image
        self.image = image
    
    def measure_perf(self, start, end, name='Script'):
        """Measures performance of a piece of code.
        
        Arguments:
            start:      getTickCount from the beggining of code snippet
            end:        getTickCount from the end of a snippet of code
        
        Returns:
            time:       Time (in seconds) that the code snippet takes to run

        Raises:
            TypeError:  Wrong Inputs
        """
        if isinstance(start, int) and isinstance(end, int):
            time = (end - start)/cv2.getTickFrequency()
        else:
            raise TypeError("Wrong Inputs, inputs need to be integer.")
        print(f'{name} took {time}s to run')
        return time

    def grayscale(self):
        pass

    def median_filter(self):
        pass

    def canny_edge_extraction(self):
        pass

    def candidate_extraction(self):
        pass

    def size_filter(self):
        pass

    def export(self):
        pass