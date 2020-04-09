import cv2
from multiprocessing import shared_memory
import numpy as np

existing_shm = shared_memory.SharedMemory(name='dataPass')
c = np.ndarray((480, 640, 3), dtype=np.uint8, buffer=existing_shm.buf)
while True:
    cv2.imshow("frame", c)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
