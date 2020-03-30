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
from imutils import contours
import imutils
import cv2
import matplotlib
import numpy as np


class Video:
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
    def __init__(self, id, camera_number):
        """Initializes the class and calls its methods."""
        self.id = id
        self.camera_number = camera_number
        self.create_video_object()

    def create_video_object(self):
        """Creates VideoCapture object."""
        self.VideoFeed = cv2.VideoCapture(self.camera_number)
        return self.VideoFeed

    def read_next_video_frame(self):
        """Reads a current frame from the camera."""
        success, frame = self.VideoFeed.read()
        if success:
            return frame
        else:
            print("Problem occured getting next frame")

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
    def __init__(self, id, video_instance):
        """Initializes the class and calls its methods."""
        self.id = id
        self.tick_init = cv2.getTickCount()
        self.video_instance = video_instance
        self.image_raw = video_instance.read_next_video_frame()
        self.image = None
        self.ROI_panel = None
        self.ROI_buttons = None
        self.sorted_label = None
    
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

    def adjust_brightness_dynamic(self):
        self.image = imutils.adjust_brightness_contrast(self.image,0,0)
    
    def grayscale(self):
        self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)

    def median_filter(self, kernelsize = 3):
        self.image = cv2.medianBlur(self.image, kernelsize)

    def canny_edge_extraction(self, sigma = 0.33):
        self.edges = imutils.auto_canny(self.image, sigma)
        self.edges = cv2.dilate(self.edges, None, iterations=1)
        self.edges = cv2.erode(self.edges, None, iterations=1)

    def candidate_extraction(self):
        cnts = cv2.findContours(self.edges, mode = cv2.RETR_EXTERNAL, method = cv2.CHAIN_APPROX_SIMPLE)
        print(cnts[0][0])
        cnts = imutils.grab_contours(cnts)
        for (i, c) in enumerate(cnts):
            self.orig_label = contours.label_contour(self.image, c, i, color= [240, 0, 159])
        (cnts, boundingBoxes) = contours.sort_contours(cnts, method = "bottom-to-top")
        clone = self.image.copy()
        for (i, c) in enumerate(cnts):
            self.sorted_label = contours.label_contour(clone, c, i, color= [240, 0, 159])

    def size_filter(self):

        pass

    def export(self):
        pass
    
    def show(self, name, frame = False):
        cv2.imshow(name,frame)

    def cleanup(self):
        """Cleanup used resources."""
        print("Cleaning up resources.")
        self.video_instance.VideoFeed.release()
        cv2.destroyAllWindows()

    def run(self):
        """A method made to be looped indefinitely."""
        try:
            pass
        except:
            pass
        else:
            while True:
                start = cv2.getTickCount()
                self.image = self.video_instance.read_next_video_frame()
                self.show("raw", self.image)
                self.adjust_brightness_dynamic()
                self.show("adj_brt", self.image)
                self.grayscale()
                self.show("gray", self.image)
                self.median_filter(kernelsize = 3)
                self.show("median", self.image)
                self.canny_edge_extraction(sigma = 0.33)
                self.show("edges", self.edges)
                self.candidate_extraction()
                self.show("cnts", self.orig_label)
                if not self.sorted_label is None:
                    self.show("cnts_sorted", self.sorted_label)
                end = cv2.getTickCount()
                #self.measure_perf(start,end)
                if cv2.waitKey(1) & 0xFF == ord("q"):
                    break
        finally:
            self.cleanup()

def main():
    cap = Video(id = 1, camera_number = 0)
    loop = Preprocess(id = 1, video_instance = cap)
    loop.run()



if __name__ == "__main__":
    main()