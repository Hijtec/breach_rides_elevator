# This Python file uses the following encoding: utf-8
import sys
from PySide2.QtWidgets import QApplication, QMainWindow, QWidget
from PySide2.QtCore import QFile
from PySide2.QtUiTools import QUiLoader




class dashboard(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    ui_file = QFile("mainwindow.ui")
    ui_file.open(QFile.ReadOnly)

    loader = QUiLoader()
    window = loader.load(ui_file)
    print(window.__dict__)
    window.label1.setText("NOICE")
    ui_file.close()
    #window = dashboard()
    window.show()
    sys.exit(app.exec_())
