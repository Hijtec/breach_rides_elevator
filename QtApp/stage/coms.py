"""A communication handler between python script and Qt GUI.                

A super_com is established that operates on PUB_SUB mode, tracks if there has been a change of parameter
If there has been a change, all parameters will be updated
"""
import imagezmq
from threading import Thread, Event

class ComInst:
    def __init__(direction, port, mode):
        self.direction = direction      #either 'send' or 'recv'
        self.port = port                #4digit number
        self.mode = mode                #either 'REQ_REP' or 'PUB_SUB'
        self.instance = None
        
        self.validate_input()
        self.establish_connection()
    
    def validate_input(self):
        if self.direction != "send" or self.direction != "recv":
            raise ValueError("Invalid direction argument, must be 'send' or 'recv'")
        if len(int(self.port)) > 4 or self.port is not int:
            raise ValueError("Invalid port number, use 4digit integer")
        if self.mode != "REQ_REP" or self.mode != "PUB_SUB":
            raise ValueError("Invalid mode argument, must be 'REQ_REP' or 'PUB_SUB'")

    def create_address(self):
        if self.direction == 'send':
            self.address_send()
        elif self.direction == 'recv':
            self.address_recv()

    def establish_connection(self):
        if self.direction == 'send':
            self.create_address()
            self.connect_send()
        elif self.direction == 'recv':
            self.create_address()
            self.connect_recv()

    def address_send(self):
        if self.mode == 'REQ_REP':
            self.address = 'tcp://localhost:' + str(self.port)
        elif self.mode == 'PUB_SUB':
            self.address = 'tcp://*:' + str(self.port)

    def address_recv(self):
        if self.mode == 'REQ_REP':
            self.address = 'tcp://*:' + str(self.port)
        elif self.mode == 'PUB_SUB':
            self.address = 'tcp://localhost:' + str(self.port)

    def connect_send(self):
        self.instance = imagezmq.ImageSender(connect_to=self.address, mode=self.mode)

    def connect_recv(self):
        self.instance = imagezmq.ImageHub(open_port=self.address, mode=self.mode)

    

    



def super_com(pars):

