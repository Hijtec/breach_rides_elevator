import cv2
import imagezmq
from threading import Thread

src_image = None
image_hub = imagezmq.ImageHub(open_port='tcp://*:5555',REQ_REP=True)
def readnext_req_rep(image_hub):
    global src_name, src_image
    src_name, src_image = image_hub.recv_image()
    image_hub.send_reply(b'OK')

def main():
    while True:
        readnext_req_rep(image_hub)
        #if src_image is not None:
        cv2.imshow("client1", src_image)
        cv2.waitKey(1)

if __name__ == "__main__":
    main()