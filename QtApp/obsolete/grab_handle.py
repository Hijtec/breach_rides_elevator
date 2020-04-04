# This Python file uses the following encoding: utf-8
import cv2
from multiprocessing import shared_memory
import numpy as np
import time



class Video:
        def __init__(self, id, camera_number):
                """Initializes the class and calls its methods."""
                self.id = id
                self.camera_number = camera_number
                self.create_video_object()
                self.frame = None

        def create_video_object(self):
                """Creates VideoCapture object."""
                self.VideoFeed = cv2.VideoCapture(self.camera_number)
                return self.VideoFeed

        def read_next_video_frame(self):
                """Reads a current frame from the camera."""
                self.VideoFeed.grab()
                success, self.frame = self.VideoFeed.retrieve()
                if success:
                        return self.frame
                else:
                        print("Problem occured getting next frame")

                
videoObject = Video(id = 1, camera_number = 0)
frame = videoObject.read_next_video_frame()

time.sleep(5)

#frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
print(frame)
"""
print(a.nbytes)
print(a.dtype)
print(a.shape)
"""
while True:
        frame = videoObject.read_next_video_frame()
        a = np.array(frame)
        shm = shared_memory.SharedMemory(name='dataPass', create=True, size=a.nbytes)
        b = np.ndarray(a.shape, dtype=a.dtype, buffer=shm.buf)
        print(shm.buf)
        b[:] = a[:] 
        shm.close()



