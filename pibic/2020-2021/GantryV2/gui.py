from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from canvas import *
from model import *
from scipy.optimize import linprog
np.set_printoptions(threshold=np.inf, linewidth=np.inf, suppress=True)

class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.setWindowTitle("Gantry Limit Analysis")
        self.setGeometry(100, 100, 640, 640)

        self.canvas = Canvas(parent=self)
        self.model = Model()

        self.setScaleWindow = SetScaleWindow(parent=self)
        self.setGridWindow = SetGridWindow(parent=self)
        self.setPropertiesWindow = SetPropertiesWindow(parent=self)
        self.saveWindow = SaveWindow(parent=self)
        self.reliabilityWindow = ReliabilityWindow(parent=self)

        self.canvas.setModel(self.model)

        self._createActions()
        self._createMenuBar()
        self._createToolBars()
        self._connectActions()

        self.setCentralWidget(self.canvas)

        self.canvas.setMouseTracking(True)
    
    def _createActions(self):
        self.openAction = QAction('Open', self)
        self.saveAction = QAction('Save', self)

        self.openAction.setShortcut('Ctrl+O')
        self.saveAction.setShortcut('Ctrl+S')

        self.setScaleAction = QAction('Scale', self)
        self.setGridAction = QAction('Grid', self)

        self.limitAnalisysAction = QAction('Limit Analysis', self)
        self.reliabilityAnalisysAction = QAction('Reliability Analysis', self)

        self.drawAction = QAction('Draw', self, checkable=True)
        self.addRestraintsAction = \
            QAction('Add Restraints', self, checkable=True)
        self.addLoadsAction = QAction('Add Loads', self, checkable=True)

        group = QActionGroup(self)
        group.setExclusive(True)
        group.addAction(self.drawAction)
        group.addAction(self.addRestraintsAction)
        group.addAction(self.addLoadsAction)

        self.propertiesAction = QAction('Properties', self)

        self.delNodeAction = QAction('Del Node', self)
        self.delElementAction = QAction('Del Element', self)

    def _createMenuBar(self):
        menuBar = QMenuBar(self)
        self.setMenuBar(menuBar)

        fileMenu = menuBar.addMenu('File')
        settingsMenu = menuBar.addMenu('Settings')
        runMenu = menuBar.addMenu('Run')

        fileMenu.addAction(self.openAction)
        fileMenu.addAction(self.saveAction)

        settingsMenu.addAction(self.setScaleAction)
        settingsMenu.addAction(self.setGridAction)

        runMenu.addAction(self.limitAnalisysAction)
        runMenu.addAction(self.reliabilityAnalisysAction)
    
    def _createToolBars(self):
        self.toolBar = self.addToolBar("Toolbar")
        self.toolBar.addAction(self.drawAction)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.addRestraintsAction)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.addLoadsAction)
        self.toolBarDoubleSpinBox = QDoubleSpinBox()
        self.toolBarDoubleSpinBox.setSingleStep(0.1)
        self.toolBarDoubleSpinBox.setMinimum(-1000)
        self.toolBarDoubleSpinBox.setMaximum(1000)
        self.toolBar.addWidget(self.toolBarDoubleSpinBox)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.propertiesAction)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.delNodeAction)
        self.toolBar.addAction(self.delElementAction)

    def _connectActions(self):
        self.openAction.triggered.connect(self.openFunction)
        self.saveAction.triggered.connect(self.saveFunction)

        self.setScaleAction.triggered.connect(self.setScaleFunction)
        self.setGridAction.triggered.connect(self.setGridFunction)
        
        self.limitAnalisysAction.triggered.connect \
            (self.limitAnalisysFunction)
        self.reliabilityAnalisysAction.triggered.connect \
            (self.reliabilityAnalisysFunction)

        self.drawAction.triggered.connect(self.drawMode)
        self.addRestraintsAction.triggered.connect(self.addRestraintsMode)
        self.addLoadsAction.triggered.connect(self.addLoadsMode)
        self.propertiesAction.triggered.connect(self.setProperties)

        self.delNodeAction.triggered.connect(self.delNodeFunction)
        self.delElementAction.triggered.connect(self.delElementFunction)
    
    def openFunction(self):
        try:
            fileName = QFileDialog.getOpenFileName()[0]
            self.model.fromJSON(fileName)
        except Exception:
            pass

    def saveFunction(self):
        try:
            self.saveWindow.show()
        except Exception:
            pass
    
    def setScaleFunction(self):
        self.setScaleWindow.show()
    
    def setGridFunction(self):
        self.setGridWindow.show()
    
    def drawMode(self):
        self.model.eraseBrokenElements()
        self.canvas.setMode('Draw')
    
    def addRestraintsMode(self):
        self.canvas.setMode('Restraints')
    
    def addLoadsMode(self):
        self.canvas.setMode('Loads')

    def setProperties(self):
        self.setPropertiesWindow.doubleSpinBox1.setValue \
            (self.model.compressionLimit)
        self.setPropertiesWindow.doubleSpinBox2.setValue \
            (self.model.tractionLimit)
        self.setPropertiesWindow.doubleSpinBox3.setValue \
            (self.model.momentLimit)
            
        self.setPropertiesWindow.label4.setText('')
        self.setPropertiesWindow.show()

    def delNodeFunction(self):
        self.model.delNode()
        self.canvas.update()

    def delElementFunction(self):
        self.model.delElement()
        self.canvas.update()

    def limitAnalisysFunction(self):
        nodesCoordinates = [[node.x, node.y] for node in self.model.nodes]
        restraints = [[int(n.xRestraint), int(n.yRestraint), int(n.momentRestraint)] for n in self.model.nodes]
        loads = [[n.xLoad, n.yLoad, n.moment] for n in self.model.nodes]
        connectivity = [[self.model.nodes.index(element.n1), self.model.nodes.index(element.n2)] for element in self.model.elements]
        elementProperties = [-self.model.compressionLimit, self.model.tractionLimit]
        momentCapacity = self.model.momentLimit

        degreesOfFreedom = 3
        numInternalForces = 3
        numNodes = len(nodesCoordinates)
        numElements = len(connectivity)
        numEquations = numNodes * degreesOfFreedom
        numVariables = 1 + numElements * numInternalForces

        objectiveFunction = np.zeros(numVariables)
        objectiveFunction[0] = -1

        A = np.zeros((numEquations, numVariables))
        lambdaColumn = np.reshape(loads, newshape=-1)
        A[:, 0] = lambdaColumn
        for i, element in enumerate(connectivity):
            node1, node2 = element
            x1, y1 = nodesCoordinates[node1]
            x2, y2 = nodesCoordinates[node2]
            deltaX = x2 - x1
            deltaY = y2 - y1
            L = np.sqrt(deltaX ** 2 + deltaY ** 2)
            cosTheta = deltaX / L
            sinTheta = deltaY / L
            values = np.array([
                [-cosTheta, -sinTheta/L, -sinTheta/L],
                [-sinTheta,  cosTheta/L,  cosTheta/L],
                [        0,           1,           0],
                [ cosTheta,  sinTheta/L,  sinTheta/L],
                [ sinTheta, -cosTheta/L, -cosTheta/L],
                [        0,           0,           1]])
            rows = [node1 * 3, node1 * 3 + 1, node1 * 3 + 2, node2 * 3, node2 * 3 + 1, node2 * 3 + 2]
            A[rows, i * 3 + 1:i * 3 + 4] = - values
        restraintsReshaped = np.reshape(restraints, newshape=-1)
        indexesToBeDeleted = [index for index, value in enumerate(restraintsReshaped) if value == 1]
        A = np.delete(A, indexesToBeDeleted, axis=0)

        b = np.zeros(len(A))

        normalBounds = elementProperties
        momentBounds = [-momentCapacity, momentCapacity]

        bounds = [[0, None]] + [normalBounds, momentBounds, momentBounds] * numElements

        results = linprog(objectiveFunction, A_eq=A, b_eq=b, bounds=bounds)
        solution = results.x
        self.model.solution = solution
        solutionLambda = solution[0]

        self.model.brokenElements = []
        if solutionLambda < 1:
            internalForces = solution[1:]
            elementsBounds = np.array(bounds[1:])
            for i in range(numElements):
                condition1 = (elementsBounds[i*3][0] < round(internalForces[i*3], 5) < elementsBounds[i*3][1])
                condition2 = (elementsBounds[i*3+1][0] < round(internalForces[i*3+1], 5) < elementsBounds[i*3+1][1])
                condition3 = (elementsBounds[i*3+2][0] < round(internalForces[i*3+2], 5) < elementsBounds[i*3+2][1])
                if (condition1 and condition2 and condition3):
                    self.model.brokenElements.append(False)
                else:
                    self.model.brokenElements.append(True)
        
        self.resultsWindow = LimitResultsWindow(parent=self)
        self.resultsWindow.show()

    def reliabilityAnalisysFunction(self):
        try:
            self.reliabilityWindow.show()
        except Exception:
            pass

class SetScaleWindow(QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.parent = parent

        self.setWindowTitle('Scale')
        self.setGeometry(100, 100, 0, 0)

        layout = QVBoxLayout()
        sublayout1 = QHBoxLayout()
        sublayout2 = QHBoxLayout()

        label1 = QLabel('1 m = ')
        self.spinBox = QSpinBox()
        self.spinBox.setMaximum(1024)
        self.spinBox.setValue(self.parent.canvas.scale)
        label2 = QLabel(' pixels')
        button1 = QPushButton('Half')
        button2 = QPushButton('Double')
        button3 = QPushButton('Apply')

        button1.clicked.connect(self.half)
        button2.clicked.connect(self.double)
        button3.clicked.connect(self.apply)

        sublayout1.addWidget(label1)
        sublayout1.addWidget(self.spinBox)
        sublayout1.addWidget(label2)
        sublayout2.addWidget(button1)
        sublayout2.addWidget(button2)

        layout.addLayout(sublayout1)
        layout.addLayout(sublayout2)
        layout.addWidget(button3)

        centralWidget = QWidget()
        centralWidget.setLayout(layout)
        self.setCentralWidget(centralWidget)
    
    def half(self):
        self.spinBox.setValue(self.spinBox.value()/2)
        self.parent.canvas.setScale(self.spinBox.value())

    def double(self):
        self.spinBox.setValue(self.spinBox.value()*2)
        self.parent.canvas.setScale(self.spinBox.value())
    
    def apply(self):
        self.parent.canvas.setScale(self.spinBox.value())

class SetGridWindow(QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.parent = parent

        self.setWindowTitle('Grid')
        self.setGeometry(100, 100, 0, 0)

        layout = QVBoxLayout()
        sublayout1 = QHBoxLayout()
        sublayout2 = QHBoxLayout()

        label = QLabel('Grid spacing: ')
        self.spinBox = QSpinBox()
        self.spinBox.setMaximum(1024)
        self.spinBox.setValue(self.parent.canvas.gridSpacing)
        button1 = QPushButton('Half')
        button2 = QPushButton('Double')
        button3 = QPushButton('Apply')

        button1.clicked.connect(self.half)
        button2.clicked.connect(self.double)
        button3.clicked.connect(self.apply)

        sublayout1.addWidget(label)
        sublayout1.addWidget(self.spinBox)
        sublayout2.addWidget(button1)
        sublayout2.addWidget(button2)
        layout.addLayout(sublayout1)
        layout.addLayout(sublayout2)
        layout.addWidget(button3)

        centralWidget = QWidget()
        centralWidget.setLayout(layout)
        self.setCentralWidget(centralWidget)
    
    def half(self):
        self.spinBox.setValue(self.spinBox.value()/2)
        self.parent.canvas.setGridSpacing(self.spinBox.value())

    def double(self):
        self.spinBox.setValue(self.spinBox.value()*2)
        self.parent.canvas.setGridSpacing(self.spinBox.value())
    
    def apply(self):
        self.parent.canvas.setGridSpacing(self.spinBox.value())

class SetPropertiesWindow(QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.parent = parent

        self.setWindowTitle('Properties')
        self.setGeometry(100, 100, 0, 0)

        layout = QVBoxLayout()
        sublayout = QGridLayout()

        label1 = QLabel('Compression Limit: ')
        label2 = QLabel('Tension Limit: ')
        label3 = QLabel('Moment Limit: ')
        self.doubleSpinBox1 = QDoubleSpinBox()
        self.doubleSpinBox2 = QDoubleSpinBox()
        self.doubleSpinBox3 = QDoubleSpinBox()
        self.doubleSpinBox1.setMaximum(1000)
        self.doubleSpinBox2.setMaximum(1000)
        self.doubleSpinBox3.setMaximum(1000)
        self.doubleSpinBox1.setSingleStep(0.1)
        self.doubleSpinBox2.setSingleStep(0.1)
        self.doubleSpinBox3.setSingleStep(0.1)

        button = QPushButton('Apply')
        button.clicked.connect(self.apply)

        self.label4 = QLabel('')

        sublayout.addWidget(label1, 0, 0)
        sublayout.addWidget(self.doubleSpinBox1, 0, 1)
        sublayout.addWidget(label2, 1, 0)
        sublayout.addWidget(self.doubleSpinBox2, 1, 1)
        sublayout.addWidget(label3, 2, 0)
        sublayout.addWidget(self.doubleSpinBox3, 2, 1)

        layout.addLayout(sublayout)
        layout.addWidget(button)
        layout.addWidget(self.label4)

        centralWidget = QWidget()
        centralWidget.setLayout(layout)
        self.setCentralWidget(centralWidget)
    
    def apply(self):
        self.parent.model.setCompressionLimit(self.doubleSpinBox1.value())
        self.parent.model.setTractionLimit(self.doubleSpinBox2.value())
        self.parent.model.setMomentLimit(self.doubleSpinBox3.value())
        self.label4.setText('Changes saved!')
        # self.label4.setAlignment(Qt.Alignment.AlignCenter)
        timer = QTimer()
        timer.singleShot(2000, lambda: self.label4.setText(''))

class SaveWindow(QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.parent = parent

        self.setWindowTitle('Save')
        self.setGeometry(100, 100, 250, 0)

        layout = QVBoxLayout()
        sublayout = QHBoxLayout()

        label1 = QLabel('File name: ')
        self.lineEdit = QLineEdit()
        button1 = QPushButton('Save JSON')
        button2 = QPushButton('Save IFC')
        self.label2 = QLabel('')

        button1.clicked.connect(self.saveJSON)
        button2.clicked.connect(self.saveIFC)
        
        sublayout.addWidget(label1)
        sublayout.addWidget(self.lineEdit)
        layout.addLayout(sublayout)
        layout.addWidget(button1)
        layout.addWidget(button2)
        layout.addWidget(self.label2)
        
        centralWidget = QWidget()
        centralWidget.setLayout(layout)
        self.setCentralWidget(centralWidget)

    def saveJSON(self):
        self.parent.model.toJSON(self.lineEdit.text())
        self.label2.setText('JSON file saved in current directory!')
        # self.label2.setAlignment(Qt.Alignment.AlignCenter)
        timer = QTimer()
        timer.singleShot(3000, lambda: self.label2.setText(''))
    
    def saveIFC(self):
        self.parent.model.toIFC(self.lineEdit.text())
        self.label2.setText('IFC file saved in current directory!')
        # self.label2.setAlignment(Qt.Alignment.AlignCenter)
        timer = QTimer()
        timer.singleShot(3000, lambda: self.label2.setText(''))

class ReliabilityWindow(QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.parent = parent

        self.setWindowTitle('Reliability Analysis')
        self.setGeometry(100, 100, 250, 0)

        self.model = parent.model

        layout = QVBoxLayout()
        sublayout = QGridLayout()

        numberOfTests = 0
        label1 = QLabel('Loads std: ')
        label2 = QLabel('Normal stress limit std: ')
        label3 = QLabel('Moment capacity std: ')
        label4 = QLabel('Number of tests: ')
        self.label5 = QLabel('Failure rate: 0 %')
        self.lineEdit1 = QLineEdit()
        self.lineEdit2 = QLineEdit()
        self.lineEdit3 = QLineEdit()
        self.lineEdit4 = QLineEdit()
        button1 = QPushButton('Run')

        button1.clicked.connect(self.run)
        
        sublayout.addWidget(label1, 0, 0)
        sublayout.addWidget(self.lineEdit1, 0, 1)
        sublayout.addWidget(label2, 1, 0)
        sublayout.addWidget(self.lineEdit2, 1, 1)
        sublayout.addWidget(label3, 2, 0)
        sublayout.addWidget(self.lineEdit3, 2, 1)
        sublayout.addWidget(label4, 3, 0)
        sublayout.addWidget(self.lineEdit4, 3, 1)

        layout.addLayout(sublayout)
        layout.addWidget(self.label5)
        layout.addWidget(button1)
        
        centralWidget = QWidget()
        centralWidget.setLayout(layout)
        self.setCentralWidget(centralWidget)
    
    def run(self):
        loadsStd = float(self.lineEdit1.text())
        propertiesStd = float(self.lineEdit2.text())
        momentCapacityStd = float(self.lineEdit3.text())
        numberOfTests = int(self.lineEdit4.text())

        nodesCoordinates = [[node.x, node.y] for node in self.model.nodes]
        restraints = [[int(n.xRestraint), int(n.yRestraint), int(n.momentRestraint)] for n in self.model.nodes]
        loads = [[node.xLoad, node.yLoad, node.moment] for node in self.model.nodes]
        connectivity = [[self.model.nodes.index(element.n1), self.model.nodes.index(element.n2)] for element in self.model.elements]
        elementProperties = [-self.model.compressionLimit, self.model.tractionLimit]
        momentCapacity = self.model.momentLimit

        degreesOfFreedom = 3
        numInternalForces = 3
        numNodes = len(nodesCoordinates)
        numElements = len(connectivity)
        numEquations = numNodes * degreesOfFreedom
        numVariables = 1 + numElements * numInternalForces

        objectiveFunction = np.zeros(numVariables)
        objectiveFunction[0] = -1

        A = np.zeros((numEquations, numVariables))
        for i, element in enumerate(connectivity):
            node1, node2 = element
            x1, y1 = nodesCoordinates[node1]
            x2, y2 = nodesCoordinates[node2]
            deltaX = x2 - x1
            deltaY = y2 - y1
            L = np.sqrt(deltaX ** 2 + deltaY ** 2)
            cosTheta = deltaX / L
            sinTheta = deltaY / L
            values = np.array([
                [-cosTheta, -sinTheta/L, -sinTheta/L],
                [-sinTheta,  cosTheta/L,  cosTheta/L],
                [        0,           1,           0],
                [ cosTheta,  sinTheta/L,  sinTheta/L],
                [ sinTheta, -cosTheta/L, -cosTheta/L],
                [        0,           0,           1]])
            rows = [node1 * 3, node1 * 3 + 1, node1 * 3 + 2, node2 * 3, node2 * 3 + 1, node2 * 3 + 2]
            A[rows, i * 3 + 1:i * 3 + 4] = - values
        restraintsReshaped = np.reshape(restraints, newshape=-1)
        indexesToBeDeleted = [index for index, value in enumerate(restraintsReshaped) if value == 1]
        A = np.delete(A, indexesToBeDeleted, axis=0)

        b = np.zeros(len(A))

        numFailures = 0
        for i in range(numberOfTests):
            updatedLoads = np.reshape(np.random.normal(loads, scale=loadsStd), -1)
            updatedLoads = np.delete(updatedLoads, indexesToBeDeleted, axis=0)

            A[:, 0] = updatedLoads
            
            bounds = [[0, None]]
            for j in range(numElements):
                updatedProperties = np.random.normal(elementProperties, scale=propertiesStd)
                updatedMomentCapacity = np.random.normal(momentCapacity, scale=momentCapacityStd)
                
                normalBounds = updatedProperties
                momentBounds = [-updatedMomentCapacity, updatedMomentCapacity]

                bounds.append(normalBounds)
                bounds.append(momentBounds)
                bounds.append(momentBounds)

            results = linprog(objectiveFunction, A_eq=A, b_eq=b, bounds=bounds)
            solution = results.x
            solutionLambda = solution[0]

            if solutionLambda < 1:
                numFailures += 1
        
        self.label5.setText(f'Failure rate: {numFailures / numberOfTests:.2f} %')

class LimitResultsWindow(QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.parent = parent
        self.setWindowTitle('Limit Analisys Results')
        self.setGeometry(100, 100, 0, 0)

        layout = QGridLayout()
        table = QTableWidget()
        table.setRowCount(len(self.parent.model.solution))
        table.setColumnCount(2)

        for i, value in enumerate(self.parent.model.solution):
            variable = QTableWidgetItem(f'x{i+1}:')
            value = QTableWidgetItem(str(round(value, 5)))
            table.setItem(i, 0, variable)
            table.setItem(i, 1, value)

        layout.addWidget(table)

        centralWidget = QWidget()
        centralWidget.setLayout(layout)
        self.setCentralWidget(centralWidget)
