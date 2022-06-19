from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.Qt import *
from gantry import *
from drawingTool import *
from limitAnalysis import *

class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.secondWindow = None

        self.setWindowTitle("Gantry Limit Analysis")
        self.setGeometry(100, 100, 800, 600)

        self.layout = QVBoxLayout()
        self.subLayout1 = QHBoxLayout()
        self.subLayout2 = QHBoxLayout()
        self.subLayout3 = QHBoxLayout()

        self.centralWidget = QWidget()

        self.button1 = QPushButton('OPEN JSON FILE')
        self.button2 = QPushButton('LIMIT ANALYSIS')

        self.label1 = QLabel()
        self.label2 = QLabel('COMPRESSION BOUND:')
        self.label3 = QLabel('TRACTION BOUND:')
        self.label4 = QLabel('MOMENT CAPACITY:')

        self.doubleSpinBox1 = QDoubleSpinBox()
        self.doubleSpinBox2 = QDoubleSpinBox()
        self.doubleSpinBox3 = QDoubleSpinBox()

        self.doubleSpinBox1.setSingleStep(0.1)
        self.doubleSpinBox2.setSingleStep(0.1)
        self.doubleSpinBox3.setSingleStep(0.1)
        
        self.setStatusBar(QStatusBar(self))

        self.subLayout1.addWidget(self.label2)
        self.subLayout1.addWidget(self.doubleSpinBox1)

        self.subLayout2.addWidget(self.label3)
        self.subLayout2.addWidget(self.doubleSpinBox2)

        self.subLayout3.addWidget(self.label4)
        self.subLayout3.addWidget(self.doubleSpinBox3)

        self.layout.addWidget(self.button1)
        self.layout.addWidget(self.label1)
        self.layout.addLayout(self.subLayout1)
        self.layout.addLayout(self.subLayout2)
        self.layout.addLayout(self.subLayout3)
        self.layout.addWidget(self.button2)

        self.centralWidget.setLayout(self.layout)

        self.setCentralWidget(self.centralWidget)

        self.label1.setAlignment(Qt.AlignHCenter)
        self.label2.setAlignment(Qt.AlignRight | Qt.AlignCenter)
        self.label3.setAlignment(Qt.AlignRight | Qt.AlignCenter)
        self.label4.setAlignment(Qt.AlignRight | Qt.AlignCenter)

        self.label1.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.MinimumExpanding)
        self.label1.setScaledContents(True)

        self.button1.setStatusTip('Open JSON file')
        self.button2.setStatusTip('Monte Carlo Reliability Analysis')

        self.button1.clicked.connect(self.button1_clicked)
        self.button2.clicked.connect(self.button2_clicked)
        
        self.gantry = None

    def reset(self):
        self.label1.setText(' ')
        self.doubleSpinBox1.setValue(0)
        self.doubleSpinBox2.setValue(0)
        self.doubleSpinBox3.setValue(0)
        self.gantry = None

    def button1_clicked(self):
        try:
            jsonFilePath = QFileDialog.getOpenFileName()[0]

            self.gantry = Gantry()
            self.gantry.fromJson(jsonFilePath)

            drawingTool = DrawingTool()
            drawingTool.plotStructure(self.gantry)
            imagePath = drawingTool.getPath('gantryPreview')

            self.label1.setPixmap(QPixmap(imagePath))

            maxCompression, maxTraction = self.gantry.elementProperties
            momentCapacity = self.gantry.momentCapacity

            self.doubleSpinBox1.setValue(abs(maxCompression))
            self.doubleSpinBox2.setValue(maxTraction)
            self.doubleSpinBox3.setValue(momentCapacity)

        except Exception as erro:
            self.reset()
            dlg = ErrorDialog(erro)
            dlg.exec_()
    
    def button2_clicked(self):
        try:
            maxCompression = -self.doubleSpinBox1.value()
            maxTraction = self.doubleSpinBox2.value()
            momentCapacity = self.doubleSpinBox3.value()

            self.gantry.setElementProperties((maxCompression, maxTraction))
            self.gantry.setMomentCapacity(momentCapacity)

            solution, brokenElements = limitAnalysis(self.gantry)

            drawingTool = DrawingTool()
            drawingTool.plotStructure(self.gantry, brokenElements)
            imagePath = drawingTool.getPath('gantryResult')
            self.label1.setPixmap(QPixmap(imagePath))

            self.secondWindow = SecondWindow(solution)
            self.secondWindow.show()

        except Exception as erro:
            self.reset()
            dlg = ErrorDialog(erro)
            dlg.exec_()

class SecondWindow(QWidget):

    def __init__(self, solution, parent=None):
        super().__init__(parent=parent)
        
        self.setWindowTitle('Results')
        self.setGeometry(900, 100, 0, 0)

        self.layout = QVBoxLayout()

        for i, value in enumerate(solution):
            subLayout = QHBoxLayout()
            variable = QLabel(f'x{i+1}:')
            value = QLabel(str(round(value, 5)))
            subLayout.addWidget(variable)
            subLayout.addWidget(value)
            variable.setAlignment(Qt.AlignRight)
            value.setAlignment(Qt.AlignCenter)
            self.layout.addLayout(subLayout)
        
        self.setLayout(self.layout)

class ErrorDialog(QDialog):
    
    def __init__(self, erro, parent=None):
        super().__init__(parent=parent)
        self.setWindowTitle("Error")
        
        self.layout = QVBoxLayout()
        
        self.message = QLabel(str(erro).capitalize())
        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok)

        self.message.setAlignment(Qt.AlignHCenter)
        self.buttonBox.accepted.connect(self.accept)

        self.layout.addWidget(self.message)
        self.layout.addWidget(self.buttonBox)        

        self.setLayout(self.layout)
