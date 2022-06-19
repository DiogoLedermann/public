from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from mycanvas import *
from mymodel import *

class MyWindow(QMainWindow):

    def __init__(self):
        super(MyWindow, self).__init__()
        self.setGeometry(100,100,600,400)
        self.setWindowTitle("MyGLDrawer")
        self.canvas = MyCanvas()
        self.setCentralWidget(self.canvas)
        # create a model object and pass it to canvas object
        self.model = MyModel()
        self.canvas.setModel(self.model)
        # create a Toolbar
        tb = self.addToolBar("File")
        fit = QAction(QIcon("curve_colector/icons/fit.jpg"),"fit",self)
        tb.addAction(fit)
        tb.actionTriggered[QAction].connect(self.tbpressed)
#        tb2 = self.addToolBar("Draw")
#        line = QAction(QIcon("icons/fit.jpg"),"line",self)
#        tb2.addAction(line)

    def tbpressed(self,a):
        if a.text() == "fit":
            self.canvas.fitWorldToViewport()
        
        
