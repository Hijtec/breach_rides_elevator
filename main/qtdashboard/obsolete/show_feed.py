from PyQt5 import QtCore, QtGui, uic, QtWidgets
import sys
import cv2
import threading
import queue
from grab_handle import videoObject

app = QtWidgets.QApplication(sys.argv)
running = False
capture_thread = None
q = queue.Queue()

form_class = uic.loadUiType("test.ui")
form_class = form_class[0]

def grab(cam, queue, width, height, fps):
    global running                                          #sets global variable running

    while(running):
        img = videoObject.read_next_video_frame()
        frame = {}
        frame["img"] = img

        if queue.qsize() < 10:
            queue.put(frame)
        else:
            print(queue.qsize())


class OwnImageWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(OwnImageWidget, self).__init__(parent)        #inherits from QtWidgets.QWidget class
        self.image = None

    def setImage(self, image):
        self.image = image
        sz = image.size()           #gets QSize
        self.setMinimumSize(sz)     #The widget cannot be resized to a smaller size than the minimum widget size
        self.update()               #This function does not cause an immediate repaint; instead it schedules a PAINTEVENT for processing when Qt returns to the main event loop.

    def paintEvent(self, event):
        qp = QtGui.QPainter()       #QPainter provides highly optimized functions to do most of the drawing GUI programs require, this builts the object
        qp.begin(self)              #Begins painting the paint device and returns true if successful; otherwise returns false.
        if self.image:
            qp.drawImage(QtCore.QPoint(0, 0), self.image) #Draws the given image(self.image) at the given point (0,0)
        qp.end()

class MyWindowClass(QtWidgets.QMainWindow, form_class):
    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)                #parent = QMainWindow, inherits its methods
        self.setupUi(self)                                          #setup MyWindowClass by reading properties of QMainWindow

        self.startButton.clicked.connect(self.start_clicked)        #Call start_clicked method if you click the button

        self.window_width = self.ImgWidget.frameSize().width()      #Read QSize width property frameSize of ImgWidget object
        self.window_height = self.ImgWidget.frameSize().height()    #Read QSize height property frameSize of ImgWidget object
        self.ImgWidget = OwnImageWidget(self.ImgWidget)             #Initiate OwnImageWidget object from ImgWidget object

        self.timer = QtCore.QTimer(self)                            #Setup Qtimer object
        self.timer.timeout.connect(self.update_frame)               #Sets signal connection of Timeout to run update_frame method
        self.timer.start(1)                                         #Sets the timer to start with a timeout of 1 milisecond


    def start_clicked(self):
        global running                                              #Sets running var as global
        running = True                                              #Sets it to True
        capture_thread.start()                                      #Starts capture_thread threading object (with args and all)
        self.startButton.setEnabled(False)                          #Greys out the startButton
        self.startButton.setText('Starting...')                     #Sets the text to Starting before the camera feed connects
    
    def update_frame(self):
        if not q.empty():                                           #Checks if the algorithm has some frames grabbed in the buffer
            self.startButton.setText('Camera is live')              #Sets the startButton text to different text
            frame = q.get()                                         #Grabs the frame from the queue buffer
            img = frame["img"]                                      #Gets the array under "img" key

            img_height, img_width, img_colors = img.shape           #reads array shape
            scale_w = float(self.window_width) / float(img_width)   #scales img_width based on window_width
            scale_h = float(self.window_height) / float(img_height) #scales img_height based on windwo_height
            scale = min([scale_w, scale_h])                         #scales the minimum of width/height to preserve aspect ratio

            if scale == 0:
                scale = 1                                           #prevents the image to congregate upon a point

            img = cv2.resize(img, None, fx=scale, fy=scale, interpolation = cv2.INTER_CUBIC)    #resizes the img by scale
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)                                          #convert to RGB
            height, width, bpc = img.shape                                                      #bpc Bytes per channel
            bpl = bpc * width                                                                   #bpl Bytes per line
            image = QtGui.QImage(img.data, width, height, bpl, QtGui.QImage.Format_RGB888)      #creates an QImage object
            self.ImgWidget.setImage(image)                                                      #displays an QImage object

    def closeEvent(self, event):
        global running
        running = False

capture_thread = threading.Thread(target=grab, args = (0, q, 1920, 1080, 30))


w = MyWindowClass(None)
w.setWindowTitle('USB camera Test')
w.show()
app.exec_()
