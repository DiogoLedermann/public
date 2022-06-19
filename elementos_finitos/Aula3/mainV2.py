import sys
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import QPoint
from PyQt6.QtOpenGLWidgets import QOpenGLWidget
from OpenGL.GL import *

class MyPoint():

    def __init__(self, x, y):
        self.x = x
        self.y = y

class MyCurve():

    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2
    
    def getCoords(self):
        return self.p1.x, self.p1.y, self.p2.x, self.p2.y

class MyModel():

    def __init__(self):
        self.curves = []
    
    def getCurves(self):
        return self.curves
    
    def addCurve(self, curve):
        self.curves.append(curve)

class MyCanvas(QOpenGLWidget):
    
    def __init__(self):
        super(MyCanvas, self).__init__()
        self.width = 0
        self.height = 0
        self.model = None
        self.p1 = QPoint(0, 0)
        self.p2 = QPoint(0, 0)

    def initializeGL(self):
        glClearColor(1, 1, 1, 1)
        glClear(GL_COLOR_BUFFER_BIT)
        glEnable(GL_LINE_SMOOTH)
    
    def resizeGL(self, w, h):
        self.width = w
        self.height = h
        glViewport(0, 0, self.width, self.height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(0, self.width, self.height, 0, -1, 1)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT)
        glColor3f(1, 0, 0)
        glBegin(GL_LINES)
        glVertex2f(self.p1.x(), self.p1.y())
        glVertex2f(self.p2.x(), self.p2.y())
        curves = self.model.getCurves()
        for curve in curves:
            p1x, p1y, p2x, p2y, = curve.getCoords()
            glVertex2f(p1x, p1y)
            glVertex2f(p2x, p2y)
        glEnd()
    
    def setModel(self, model):
        self.model = model

    def mousePressEvent(self, event):
        self.p1 = event.position()

    def mouseMoveEvent(self, event):
        self.p2 = event.position()
        self.update()
    
    def mouseReleaseEvent(self, event):
        myPoint1 = MyPoint(self.p1.x(), self.p1.y())
        myPoint2 = MyPoint(self.p2.x(), self.p2.y())
        myCurve = MyCurve(myPoint1, myPoint2)
        self.model.addCurve(myCurve)

class MainWindow(QMainWindow):
    
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle('Teste')
        
        self.canvas = MyCanvas()
        self.model = MyModel()

        # self.canvas.setMouseTracking(True)

        self.canvas.setModel(self.model)

        self.setCentralWidget(self.canvas)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec())
