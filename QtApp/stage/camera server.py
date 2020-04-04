"""A camera server module to stream camera data.

#Input: User input of camera number, number of ports, port number, type of connection
#Output: User feedback in command line
#Assumptions: Camera is ready to be connected to (is not currently used)
                Only one camera is used (Would require tweaking))
                

This script creates communication interface utilizing imagezmq and its API from pyzmq
The communication interface is created as follows:
    User runs the script and is greeted by choosing a camera
    Then he chooses number of connections he wishes to establish
    Then he chooses the port numbers and modes(REQ_REP/SUB_PUB) to be used
    Accordingly, these connections will be established
    TODO: multithreading so that there can be multiple REQ_REPs
    An infinite loop will send these data streams from camera

#Issues: Due to not implementing multithreading, the data will be sync/timed as the slowest REQ_REP connection 
"""

import socket
import time
from imutils.video import VideoStream
import imagezmq

def init_sender(adress,mode):
    if not type(mode) == bool:
        raise TypeError("Mode must be a boolean.")
    if not type(adress) == str:
        raise TypeError("Adress must be a string.")
    print(f"Establishing connection {adress} with REQ_REP={mode}")
    sender = imagezmq.ImageSender(connect_to=adress,REQ_REP=mode)
    return sender

def user_interface_cam_ncon():
    cam_number = input("Camera number / default settings:")
    if cam_number == "":
        return cam_number, 0
    else:
        cam_number = int(cam_number)
        ncon = int(input("Number of connections wanted: "))
        return cam_number, ncon

def user_interface_add_mode(ncon, senders):
    for con in range(ncon):
        address = str(input(f"-----------------\nAddress of {con+1}. connection\n (eg.: tcp://localhost:5555) for REQ_REP\n (eg.: tcp://*:5555) for SUB_PUB\n"))
        mode = str(input("Mode of connection (REQ_REP = True, SUB_PUB = False):"))
        if mode == "True":
            mode = True
        elif mode == "False":
            mode = False
        else:
            raise TypeError("Mode must be either True or False.")
        sender = init_sender(address, mode)
        senders.append(sender)
    return senders

def add_mode_default():
    print("Sending on address localhost:5555 with REQ_REP mode")
    senders = imagezmq.ImageSender(connect_to='tcp://localhost:5555',REQ_REP=True)
    return senders


senders = []
cam_number, ncon = user_interface_cam_ncon()
if cam_number == "":
    senders.append(add_mode_default())
    cam_number = 0
else:
    senders = user_interface_add_mode(ncon, senders)
name = socket.gethostname()
cam = VideoStream(src=cam_number).start()
print("\nCamera active")
time.sleep(2.0)
print("\nSending data")
while True:
    image = cam.read()
    for sender in senders:
        sender.send_image(name, image)
