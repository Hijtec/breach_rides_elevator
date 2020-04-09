"""A communication handler between python script and Qt GUI.

    #Assumptions: No two coms instances are initiated with the same adress

Typical usage:
    import coms
    bundle = {
            "name"     :    "first",
            "def_value":    0,
            "direction":    "send",
            "port"     :    5565,
            "mode"     :    "REQ_REP"
            }
    name_dict = {}
    com_dict = {}
    coms.create_parameter(bundle,name_dict,com_dict)
"""
import socket
import imagezmq_modified as imagezmq

class ComInst:
    """An object initializing the communication instance.

    Attributes:
        direction:              Either 'send' or 'recv', determines client/server instance
        port:                   4digit number that serves as the port number
        mode:                   Either 'REQ_REP' or 'PUB_SUB', determines communication
        address:                An address for creation of communication instance
        instance:               The communication object instance
        name:                   Gets the hostname of the machine

    Methods:
        validate_input:         Validates the init input of class
        create_address:         Chooses the right address creator
        establish_connection:   Chooses the method of instance creation
        address_send:           Creates a valid server address
        address_recv:           Creates a valid client address
        connect_send:           Creates a server communication object
        connect_recv:           Creates a client communication object

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
        self.address = None
        #Call init functions
        self.validate_input()
        self.establish_connection()

    def validate_input(self):
        """Validates the input of class creation."""
        if self.direction != 'send' and self.direction != 'recv':
            raise ValueError("Invalid direction argument, must be 'send' or 'recv'")
        if int(self.port) > 9999:
            raise ValueError("Invalid port number, use 4digit integer")
        if self.mode != "REQ_REP" and self.mode != "PUB_SUB":
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
        """Checks whether the instance can send, if it does, send a message."""
        if self.direction == 'send':
            self.instance.send_image(self.name, msg)
        else:
            raise TypeError("This object is not able to send a message.")

    def recv(self):
        """Checks whether the instance can recieve, if it does, recieves a message."""
        if self.direction == 'recv':
            name, response = self.instance.recv_image()
            return name, response
        else:
            raise TypeError("This object is not able to recieve a message")

    def send_reply(self, msg=b'OK'):
        """Checks whether the instance can recieve and is in REQ_REP mode. If so, sends a reply."""
        if self.direction == 'recv' and self.mode == 'REQ_REP':
            self.instance.send_reply(msg)
        else:
            raise TypeError("This object is not able to send a reply")

    def close(self):
        """Closes the communication instance."""
        self.instance.close()

class Parameters:
    """An object initializing the parameters.

    Attributes:
        pars:               Dictionary of settable parameters and their current values
        def_pars:           Dictionary of default parameters (set at init) and their current value
        coms:               Dictionary with setted connection instance for each parameter key
        update_flag:         Dictionary with boolean corresponding to change of parameter value

    Methods:
        detect_update:
        update_last_pars:
        update_pars:

    Raises:
        ValueError:         When an invalid input has been detected

    Typical use:
        INIT
        pars = Parameters(pars,coms)
        IN LOOP
        pars.detect_updates()
        pars.update_parameters()
    """

    def __init__(self, pars, coms):
        """Initiates the Parameters class."""
        self.pars = pars
        self.last_pars_value = pars
        self.coms = coms
        self.update_flag = None

    def detect_updates(self):
        """Detects changes between last_pars_values and pars_values."""
        self.update_flag = {}
        for k, value in self.pars.items():
            if self.pars[k] != self.last_pars_value[k]:
                self.update_flag[k] = True
                self.last_pars_value.update(k=value)
            elif self.pars[k] == self.last_pars_value[k]:
                self.update_flag[k] = False

    def send_parameters(self):
        """Send those parameters that have their update_flag equal to True."""
        for k, com_inst in self.coms.items():
            if self.update_flag[k] is True:
                com_inst.send()

def create_parameter(bundle, names, coms):
    """Takes an established names(dict) and coms(dict) and updates it with data from bundle(dict)"""
    name = bundle["name"]
    if name in names:
        raise ValueError(f"{name} is already present")
    value = bundle["value"]
    direction = bundle["direction"]
    port = bundle["port"]
    mode = bundle["mode"]
    #instanciate
    cominst = ComInst(direction, port, mode)
    par_dict = {name:value}
    coms_dict = {name:cominst}
    #update the given values
    names.update(par_dict)
    coms.update(coms_dict)

def bundle_parameters(bundles):
    """Handles the creation of parameters and communication dictionaries."""
    par_dict = {}
    com_dict = {}
    for bundle in bundles:
        create_parameter(bundle, par_dict, com_dict)
    params = Parameters(par_dict, com_dict)
    return params
