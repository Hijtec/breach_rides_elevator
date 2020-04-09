"""dashboard: A QT GUI console that display the process of my master thesis.

Classes that transport OpenCV images from one computer to another. For example,
OpenCV images gathered by a Raspberry Pi camera could be sent to another
computer for displaying the images using cv2.imshow() or for further image
processing. See API and Usage Examples for details.
"""
import os
import sys

from PyQt5 import QtCore, QtGui, uic, QtWidgets

import cv2
import coms

class App():
    """An app instance with ui import"""
    def __init__(self):
        self.app = QtWidgets.QApplication(sys.argv)
        self.ui_path = os.path.dirname(os.path.abspath(__file__))
        self.form_class = uic.loadUiType(os.path.join(self.ui_path, "uidesign/mainwindow.ui"))[0]
App = App()

class OwnImageWidget(QtWidgets.QWidget):
    """Implents own ImageWidget based on QWidget"""
    def __init__(self, parent=None):
        """Defines initial variables and inheritence."""
        super(OwnImageWidget, self).__init__(parent)        #Inherits from QtWidgets.QWidget class
        self.image = None

    def setImage(self, image):
        """Sets the Image in ImageWidget using QPainter"""
        self.image = image
        sz_qsize = image.size()         #QSize
        self.setMinimumSize(sz_qsize)   #Widget cant be smaller than image size
        self.update()                   #Schedules a PAINTEVENT for Qt main event loop

    def paintEvent(self, __):
        """When paintEvent is induced by QT, the OwnImageWidget draws current image."""
        qtpainter = QtGui.QPainter()    #Inits QPainter instance (drawing process)
        qtpainter.begin(self)
        if self.image:
            qtpainter.drawImage(QtCore.QPoint(0, 0), self.image) #Draws image at topleft corner
        qtpainter.end()                 #Kills the QPainter instance

class Dashboard(QtWidgets.QMainWindow, App.form_class):
    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)
        self.setupUi(self)
        #INIT DEFAULT VARIABLES
        self.image_hub = None
        self.image_name = "UNKNOWN SOURCE"
        self.running = False
        self.frame = None
        #CUSTOM SLOTS AND SIGNALS
        self.pre_adjbr_toggle.toggled.connect(self.toggle_clicked)
        self.pre_adjbr_toggle.toggled.connect(self.set_qgroup_title)
        self.pre_adjbr_switch.toggled.connect(self.change_feed)
        #CUSTOM VARIABLES AND OBJECTS
        self.window_width = self.pre_ImgWidget.frameSize().width()
        self.window_height = self.pre_ImgWidget.frameSize().height()
        self.pre_ImgWidget = OwnImageWidget(self.pre_ImgWidget)
        #SCRIPT ALWAYS STARTS ON THESE
        self.open_subtab_now = "AdjustBrightness"
        self.open_subtab_last = "AdjustBrightness"
        self.open_tab_now = "Preprocessing"
        self.open_tab_last = "Preprocessing"
        #INIT PARAMETER OBJECTS
        self.pre_bundles = self.init_params(self.open_subtab_now)
        #INIT COMMUNICATION OBJECTS
        self.params = self.create_params(self.pre_bundles)
        #INIT TIMERS AND THEIR CALLS
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.timeout.connect(self.read_par_values)
        self.timer.timeout.connect(self.update_parameters)
        self.timer.start(1)

        self.slow_timer = QtCore.QTimer(self)
        self.slow_timer.timeout.connect(self.tab_changed)
        self.slow_timer.timeout.connect(self.subtab_changed)
        self.slow_timer.start(50)

    def change_feed(self):
        pass
    def opened_tab(self):
        pass
    def tab_changed(self):
        pass

    def opened_subtab(self):
        """Returns the current opened subtab."""
        subtab_name_qstring = self.subtabs.currentWidget().objectName()
        #subtab_name = subtab_name_qstring.data().decode('utf8'))
        subtab_name = subtab_name_qstring
        return subtab_name
    
    def subtab_changed(self):
        """Detects change of subtab, closes old parameters and initiates new ones."""
        if self.open_subtab_last != self.open_subtab_now:
            self.open_subtab_last = self.open_subtab_now
            self.open_subtab_now = self.opened_subtab()
            self.close_parameters()
            self.init_params(self.open_subtab_now)

    def toggle_clicked(self):
        """Handles the toggle button."""
        if self.pre_adjbr_toggle.isChecked() is True:
            self.running = True
            self.pre_adjbr_toggle.setText("Init...")

        elif self.pre_adjbr_toggle.isChecked() is False:
            self.running = False
            self.pre_adjbr_toggle.setText("Cam OFF")
            
    def update_frame(self):
        """Updates the ImgWidget with img from camera."""
        self.read_next()
        if self.frame is not None:
            img = self.frame
            self.pre_adjbr_toggle.setText("Cam ON")
            img_height, img_width, __ = img.shape
            #Scale the image to fit the window
            scale_w = float(self.window_width) / float(img_width)
            scale_h = float(self.window_height) / float(img_height)
            scale = min([scale_w, scale_h])
            if scale == 0:
                scale = 1
            img = cv2.resize(img, None, fx=scale, fy=scale, interpolation=cv2.INTER_CUBIC)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            #Adjust so its renderable by Qt
            height, width, bits_per_color = img.shape
            bits_per_line = bits_per_color * width
            image = QtGui.QImage(img.data, width, height, bits_per_line, QtGui.QImage.Format_RGB888)
            self.pre_ImgWidget.setImage(image)
    
    def set_qgroup_title(self):
        """Sets the qgroub Title"""
        self.read_next()
        self.pre_input_img.setTitle(self.img_name)


    def read_next(self):
        """Read next frame based on dashboard status."""
        if self.open_subtab_now == "AdjustBrightness":
            self.img_name, self.frame = self.camera_read_next()

    def camera_read_next(self, image_hub=None):
        """Reads the next frame from camera using image_hub object."""
        if self.image_hub is None:
            self.image_hub = coms.ComInst(direction='recv', port=5555, mode='REQ_REP')

        if self.running:
            src_name, src_image = self.image_hub.recv()
            self.image_hub.send_reply()

        if not self.running:
            src_name = "FEED NOT RUNNING"
            src_image = None
        return src_name, src_image

    def init_params(self, subtab):
        """Returns predetermined parameters based on input tab"""
        bundles = []
        if subtab == "AdjustBrightness":
            bundle_brightness = {"name":"pre_BRIGHTNESS", "value":0, 
                                "direction":"send", "port":1001, "mode":"REQ_REP"}
            bundle_contrast = {"name":"pre_CONTRAST", "value":0,
                                "direction":"send", "port":1002, "mode":"REQ_REP"}
            bundles = [bundle_brightness, bundle_contrast]
        else:
            raise ValueError("Invalid tab argument.")
        return bundles

    def create_params(self,bundles):
        """Handles the creation of parameters and communication dictionaries."""
        par_dict = {}
        com_dict = {}
        for bundle in bundles:
            coms.create_parameter(bundle, par_dict, com_dict)
        params = coms.Parameters(par_dict, com_dict)
        return params

    def update_parameters(self):
        """Calls methods to update parameters."""
        self.params.detect_updates()
        self.params.send_parameters()

    def read_par_values(self):
        """Reads the value off the doubleBoxes."""
        if self.open_subtab_now == "AdjustBrightness":
            #Brightness par (0.00 to 1.00)
            self.params.pars.update({"pre_BRIGHTNESS": float(self.pre_brightness_box.value()/100)})
            #Contrast par (0.00 to 1.00)
            self.params.pars.update({"pre_CONTRAST": float(self.pre_contrast_box.value()/100)})
    
    def close_parameters(self):
        """Closes all parameter connections."""
        for __, cominst in self.params.coms.items():
            cominst.close()

    def closeEvent(self,__):
        """Handles what happens after the window is closed."""
        self.running = False
        self.close_parameters()

if __name__ == "__main__":
    w = Dashboard(None)
    w.setWindowTitle("Testing")
    w.show()
    App.app.exec_()