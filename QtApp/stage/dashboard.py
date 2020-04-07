# This Python file uses the following encoding: utf-8
import os
import sys
import cv2
import imagezmq_modified as imagezmq
import time
import queue
from threading import Thread, Event
from PyQt5 import QtCore, QtGui, uic, QtWidgets

app = QtWidgets.QApplication(sys.argv)
running = False
capture_thread = None
ui_path = os.path.dirname(os.path.abspath(__file__))
form_class = uic.loadUiType(os.path.join(ui_path, "mainwindow.ui"))[0]
src_image = None
start_time = time.time()
image_hub = None
q = queue.Queue()

def camera_read_next(q):
    global image_hub
    global running
    global src_name, src_image

    if image_hub is None:
        image_hub = imagezmq.ImageHub(open_port='tcp://localhost:5555',mode='PUB_SUB')
    
    while running:
        frame = {}
        src_name, src_image = image_hub.recv_image()

    while not running:
        src_image = None

class OwnImageWidget(QtWidgets.QWidget):
    """Implents own ImageWidget based on QWidget"""
    def __init__(self, parent=None):
        super(OwnImageWidget, self).__init__(parent)        #inherits from QtWidgets.QWidget class
        self.image = None

    def setImage(self, image):
        self.image = image
        sz = image.size()       #QSize
        self.setMinimumSize(sz) #Widget cant be smaller than image size
        self.update()           #Schedules a PAINTEVENT for Qt main event loop

    def paintEvent(self, event):
        qp = QtGui.QPainter()   #Inits QPainter instance (drawing process)
        qp.begin(self)          #Starts 
        if self.image:
            qp.drawImage(QtCore.QPoint(0,0), self.image) #draws image beginning at topleft corner
        qp.end()                #Kills the QPainter instance

class dashboard(QtWidgets.QMainWindow, form_class):
    def __init__(self, parent = None):
        QtWidgets.QMainWindow.__init__(self, parent)
        self.setupUi(self)
        self.pre_adjbr_in_toggle.toggled.connect(self.toggle_clicked)

        self.window_width = self.ImgWidget.frameSize().width()
        self.window_height = self.ImgWidget.frameSize().height()
        self.ImgWidget = OwnImageWidget(self.ImgWidget)

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(1)

        self.firstClick = True

    def toggle_clicked(self):
        global running
        global src_image
        if self.pre_adjbr_in_toggle.isChecked() == True:
            running = True
            self.pre_adjbr_in_toggle.setText("Init...")
            try:
                capture_thread.start()
            except RuntimeError: #occurs if thread is dead
                src_image = None
                n = Thread(target=camera_read_next, args=(q,)) #create new instance if thread is dead
                n.start() #start thread
            

        elif self.pre_adjbr_in_toggle.isChecked() == False:
            running = False
            self.pre_adjbr_in_toggle.setText("Cam OFF")
            src_image = None
            

    def update_frame(self):
        global src_image
        if src_image is not None :
            """
            frame = q.get()
            img = frame["img"]
            """
            img = src_image
            self.pre_adjbr_in_toggle.setText("Cam ON")
            img_height, img_width, img_colors = img.shape
            scale_w = float(self.window_width) / float(img_width)
            scale_h = float(self.window_height) / float(img_height)
            scale = min([scale_w, scale_h])

            if scale == 0:
                scale = 1
            
            img = cv2.resize(img, None, fx=scale, fy=scale, interpolation=cv2.INTER_CUBIC)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            height, width, bits_per_color = img.shape
            bits_per_line = bits_per_color * width
            image = QtGui.QImage(img.data, width, height, bits_per_line, QtGui.QImage.Format_RGB888)
            self.ImgWidget.setImage(image)
    
    def closeEvent(self, event):
        global running
        running = False
    
capture_thread = Thread(target=camera_read_next, args=(q,))

w = dashboard(None)
w.setWindowTitle("Testing")
w.show()
app.exec_()

