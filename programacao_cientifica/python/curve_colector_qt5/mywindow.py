from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from mycanvas import *
from mymodel import *

class MyWindow(QMainWindow):

    def __init__(self):
        super(MyWindow, self).__init__()
        self.setGeometry(100,100,600,400)
        self.setWindowTitle("MyGLDrawer")

        self.gridDialogWindow = GridDialogWindow(self)

        self.canvas = MyCanvas()
        self.setCentralWidget(self.canvas)
        # create a model object and pass it to canvas object
        self.model = MyModel()
        self.canvas.setModel(self.model)
        # create a Toolbar
        tb = self.addToolBar("File")

        fit = QAction(QIcon("icons/fit.jpg"),"fit",self)
        tb.addAction(fit)

        panR = QAction(QIcon("icons/panright.jpg"),"panR",self)
        tb.addAction(panR)

        grid = QAction("Grid", self)
        tb.addAction(grid)

        tb.actionTriggered[QAction].connect(self.tbpressed)

    def tbpressed(self,a):
        if a.text() == "fit":
            self.canvas.fitWorldToViewport()
        elif a.text() == "panR":
            self.canvas.panWorldWindow(0.2, 0.0)
        elif a.text() == "Grid":
            self.gridDialogWindow.show()

class GridDialogWindow(QMainWindow):

    def __init__(self, parent):
        super(GridDialogWindow, self).__init__()

        self.parent = parent

        self.setGeometry(150, 150, 10, 10)
        self.setWindowTitle("Grid Dialog")

        self.mainLayout = QVBoxLayout()

        self.mainWidget = QWidget()
        self.dxLabel = QLabel('dx: ')
        self.dxInput = QLineEdit()
        self.dyLabel = QLabel('dy: ')
        self.dyInput = QLineEdit()
        self.saveButton = QPushButton('SAVE')

        self.mainLayout.addWidget(self.dxLabel)
        self.mainLayout.addWidget(self.dxInput)
        self.mainLayout.addWidget(self.dyLabel)
        self.mainLayout.addWidget(self.dyInput)
        self.mainLayout.addWidget(self.saveButton)

        self.dxInput.setText('100')
        self.dyInput.setText('100')

        self.saveButton.clicked.connect(self.save)

        self.mainWidget.setLayout(self.mainLayout)
        self.setCentralWidget(self.mainWidget)
    
    def save(self):
        dx = int(self.dxInput.text())
        dy = int(self.dyInput.text())
        self.parent.canvas.m_hmodel.setGridSpacing(dx, dy)
        self.parent.canvas.m_hmodel.generateGrid()
        self.parent.canvas.update()
