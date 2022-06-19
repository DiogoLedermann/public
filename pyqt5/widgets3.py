from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import sys


class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.setWindowTitle("My Awesome App")

        widget = QComboBox()
        widget.addItems(["One", "Two", "Three"])

        widget.currentIndexChanged.connect( self.index_changed )

        widget.currentIndexChanged[str].connect( self.text_changed )

        # widget.setEditable(False)

        # widget.setInsertPolicy(QComboBox.InsertAlphabetically)

        widget.setMaxCount(10)

        self.setCentralWidget(widget)


    def index_changed(self, i): # i is an int
        print(i)

    def text_changed(self, s): # s is a str
        print(s)


app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec_()