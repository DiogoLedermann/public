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
        self.temperatureDialogWindow = TemperatureDialogWindow(self)

        self.canvas = MyCanvas()
        self.setCentralWidget(self.canvas)
        self.model = MyModel()
        self.canvas.setModel(self.model)
        tb = self.addToolBar("File")

        fit = QAction(QIcon("icons/fit.jpg"),"fit",self)
        tb.addAction(fit)

        panR = QAction(QIcon("icons/panright.jpg"),"panR",self)
        tb.addAction(panR)

        grid = QAction("Grid", self)
        tb.addAction(grid)

        connect = QAction("Connect", self)
        tb.addAction(connect)

        setTemperature = QAction("Set temperature", self)
        tb.addAction(setTemperature)

        generateCC = QAction("Generate CC", self)
        tb.addAction(generateCC)

        saveJSON = QAction("Save JSON", self)
        tb.addAction(saveJSON)

        tb.actionTriggered[QAction].connect(self.tbpressed)

    def tbpressed(self,a):
        if a.text() == "fit":
            self.canvas.fitWorldToViewport()
        elif a.text() == "panR":
            self.canvas.panWorldWindow(0.2, 0.0)
        elif a.text() == "Grid":
            self.gridDialogWindow.show()
        elif a.text() == "Connect":
            self.canvas.m_hmodel.generateConnect()
        elif a.text() == "Set temperature":
            self.temperatureDialogWindow.show()
        elif a.text() == "Generate CC":
            self.canvas.m_hmodel.generateCC()
        elif a.text() == "Save JSON":
            self.canvas.m_hmodel.saveJSON()

class GridDialogWindow(QMainWindow):

    def __init__(self, parent):
        super(GridDialogWindow, self).__init__()

        self.parent = parent

        self.setGeometry(150, 150, 10, 10)
        self.setWindowTitle("Grid Dialog")

        self.mainLayout = QVBoxLayout()

        self.mainWidget = QWidget()
        self.dxLabel = QLabel('dx: ')
        self.nxInput = QLineEdit()
        self.dyLabel = QLabel('dy: ')
        self.nyInput = QLineEdit()
        self.saveButton = QPushButton('SAVE')

        self.mainLayout.addWidget(self.dxLabel)
        self.mainLayout.addWidget(self.nxInput)
        self.mainLayout.addWidget(self.dyLabel)
        self.mainLayout.addWidget(self.nyInput)
        self.mainLayout.addWidget(self.saveButton)

        self.nxInput.setText('10')
        self.nyInput.setText('10')

        self.saveButton.clicked.connect(self.save)

        self.mainWidget.setLayout(self.mainLayout)
        self.setCentralWidget(self.mainWidget)
    
    def save(self):
        nx = int(self.nxInput.text())
        ny = int(self.nyInput.text())
        self.parent.canvas.m_hmodel.setGrid(nx + 1, ny + 1)
        self.parent.canvas.update()

class TemperatureDialogWindow(QMainWindow):

    def __init__(self, parent):
        super(TemperatureDialogWindow, self).__init__()

        self.parent = parent

        self.setGeometry(150, 150, 10, 10)
        self.setWindowTitle("Temperature Dialog")

        self.mainLayout = QVBoxLayout()

        self.mainWidget = QWidget()
        self.temperatureLabel = QLabel('Temperature: ')
        self.tInput = QLineEdit()
        self.saveButton = QPushButton('SAVE')

        self.mainLayout.addWidget(self.temperatureLabel)
        self.mainLayout.addWidget(self.tInput)
        self.mainLayout.addWidget(self.saveButton)

        self.tInput.setText('0')

        self.saveButton.clicked.connect(self.save)

        self.mainWidget.setLayout(self.mainLayout)
        self.setCentralWidget(self.mainWidget)
    
    def save(self):
        t = int(self.tInput.text())
        self.parent.canvas.m_hmodel.setTemperature(self.parent.canvas.selectedPoints, t)
        self.parent.canvas.update()
