"""This module servers as a testbench to call QtObjects."""
# This Python file uses the following encoding: utf-8

import os
import sys
from PyQt5 import uic, QtWidgets

APP = QtWidgets.QApplication(sys.argv)
UI_PATH = os.path.dirname(os.path.abspath(__file__))
FORM_CLASS = uic.loadUiType(os.path.join(UI_PATH, "mainwindow.ui"))[0]

class Dashboard(QtWidgets.QMainWindow, FORM_CLASS):
    """Copies the QMainWindow class of xml and makes it a callable object."""
    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)
        self.setupUi(self)

if __name__ == "__main__":
    W = Dashboard(None)
    W.setWindowTitle("Testing")
    W.show()
    APP.exec_()
