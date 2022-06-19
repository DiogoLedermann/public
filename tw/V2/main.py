import sys
from PyQt5.QtWidgets import QApplication, QStyleFactory
from gui.gui import MainWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle(QStyleFactory.create("fusion"))
    window = MainWindow()
    window.show()
    app.exec_()
