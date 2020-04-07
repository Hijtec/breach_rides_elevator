"""A communication handler between python script and Qt GUI.

   #Assumptions: No two coms instances are initiated with the same adress

A super_com is established that operates on PUB_SUB mode, tracks if there has been a change of parameter
If there has been a change, all parameters will be updated
"""
import socket
import imagezmq_modified as imagezmq
from threading import Thread, Event

class ComInst:
    """An object initializing the communication instance.

    Attributes:
        direction:                  Either 'send' or 'recv', determines if the instance is client or server
        port:                       4digit number that serves as the port number 
        mode:                       Either 'REQ_REP' or 'PUB_SUB', determines blocking/non-blocking communication
        address:                    An address for creation of communication instance
        instance:                   The communication object instance
        name:                       Gets the hostname of the machine

    Methods:
        validate_input:             Validates the init input of class
        create_address:             Chooses the right address creator
        establish_connection:       Chooses the method of instance creation
        address_send:               Creates a valid server address
        address_recv:               Creates a valid client address
        connect_send:               Creates a server communication object
        connect_recv:               Creates a client communication object

    Raises:
        ValueError                  When an invalid input has been detected
    """

    def __init__(self, direction, port, mode):
        """Initializes the class and calls its methods."""
        self.direction = direction      #either 'send' or 'recv'
        self.port = port                #4digit number
        self.mode = mode                #either 'REQ_REP' or 'PUB_SUB'
        self.instance = None
        self.name = socket.gethostname()
        
        self.validate_input()
        self.establish_connection()
    
    def validate_input(self):
        """Validates the input of class creation."""
        if self.direction != "send" or self.direction != "recv":
            raise ValueError("Invalid direction argument, must be 'send' or 'recv'")
        if len(int(self.port)) > 4 or self.port is not int:
            raise ValueError("Invalid port number, use 4digit integer")
        if self.mode != "REQ_REP" or self.mode != "PUB_SUB":
            raise ValueError("Invalid mode argument, must be 'REQ_REP' or 'PUB_SUB'")

    def create_address(self):
        """Chooses the right address creator."""
        if self.direction == 'send':
            self.address_send()
        elif self.direction == 'recv':
            self.address_recv()

    def establish_connection(self):
        """Chooses the method of instance creation."""
        if self.direction == 'send':
            self.create_address()
            self.connect_send()
        elif self.direction == 'recv':
            self.create_address()
            self.connect_recv()

    def address_send(self):
        """Creates a valid server address."""
        if self.mode == 'REQ_REP':
            self.address = 'tcp://localhost:' + str(self.port)
        elif self.mode == 'PUB_SUB':
            self.address = 'tcp://*:' + str(self.port)

    def address_recv(self):
        """Creates a valid client address."""
        if self.mode == 'REQ_REP':
            self.address = 'tcp://*:' + str(self.port)
        elif self.mode == 'PUB_SUB':
            self.address = 'tcp://localhost:' + str(self.port)

    def connect_send(self):
        """Creates a server communication object."""
        self.instance = imagezmq.ImageSender(connect_to=self.address, mode=self.mode)

    def connect_recv(self):
        """Creates a client communication object."""
        self.instance = imagezmq.ImageHub(open_port=self.address, mode=self.mode)
    
    def send(self, msg):
        if self.direction == 'send':
            self.instance.send_image(self.name, msg)
        else:
            raise TypeError("This object is not able to send a message.")

    def recv(self)
        if self.direction == 'recv':
            name, response = self.instance.recv_image()
            return name, response
        else:
            raise TypeError("This object is not able to recieve a message")

    def send_reply(self, msg):
        if self.direction == 'send' and self.mode == 'REQ_REP':
            self.instance.send_reply(b'OK')
        else:
            raise TypeError("This object is not able to send a reply")

class Parameters:
    """An object initializing the parameters.

    Attributes:
        pars:                       Dictionary of settable parameters
        def_pars:                   Dictionary of default parameters (set at init)
        coms:                       Dictionary with setted connection instance
        updateFlag:                 Dictionary of T/F values determining which 

    Methods:
        detect_update:
        update_last_pars:
        update_pars:

    Raises:
        ValueError                  When an invalid input has been detected
    """

    def __init__(self, pars, coms):
        self.pars = pars
        self.last_pars = pars
        self.coms = coms
        self.updateFlag = None

    def detect_update(self):
        self.updateFlag = {}
        for k, v in self.pars:
            if self.pars[k] != self.last_pars[k]:
                updateFlag[k] = True
        self.update_last_pars()

    def update_last_pars(self):
        self.last_pars = pars

    def update_pars(self):
        for k, com_inst in self.coms:
            if self.updateFlag[k] == True:
                com_inst.send()

def create_parameters():
    pass
