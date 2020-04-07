import cv2
import imagezmq

image_hub2 = imagezmq.ImageHub(open_port='tcp://localhost:5555',REQ_REP=False)
while True:
    name, image = image_hub2.recv_image()
    cv2.imshow("client2", image)
    cv2.waitKey(1)