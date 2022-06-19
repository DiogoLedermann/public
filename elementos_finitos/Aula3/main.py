import sys
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6 import QtOpenGLWidgets, QtCore
from OpenGL.GL import *

class MyPoint():

    def __init__(self, x, y):
        self.m_x = x
        self.m_y = y

class MyCurve():

    def __init__(self, p1, p2):
        self.m_p1 = p1
        self.m_p2 = p2
    
    def getCoords(self):
        return self.m_p1.m_x, self.m_p1.m_y, self.m_p2.m_x, self.m_p2.m_y

class MyModel():

    def __init__(self):
        point1 = MyPoint(-0.9, -0.9)
        point2 = MyPoint(0.9, -0.9)
        point3 = MyPoint(0, 0.9)
        curve1 = MyCurve(point1, point2)
        curve2 = MyCurve(point2, point3)
        curve3 = MyCurve(point3, point1)
        self.curves = [curve1, curve2, curve3]
    
    def getCurves(self):
        return self.curves

class MyCanvas(QtOpenGLWidgets.QOpenGLWidget):
    
    def __init__(self):
        super(MyCanvas, self).__init__()
        self.m_w = 0
        self.m_h = 0
        self.m_model = None
        self.m_p1 = QtCore.QPoint(0, 0)
        self.m_p2 = QtCore.QPoint(0, 0)

    def initializeGL(self):
        glClearColor(1, 1, 1, 1)
        glClear(GL_COLOR_BUFFER_BIT)
        glEnable(GL_LINE_SMOOTH)
    
    def resizeGL(self, w, h):
        self.m_w = w
        self.m_h = h
        glViewport(0, 0, self.m_w, self.m_h)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(0, self.m_w, self.m_h, 0, -1, 1)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT)
        glColor3f(1, 0, 0)
        glBegin(GL_LINES)
        for curve in self.m_model.curves:
            x1, y1, x2, y2 = curve.getCoords()
            glVertex2f(x1, y1)
            glVertex2f(x2, y2)
        glVertex2f(self.m_p1.x(), self.m_p1.y())
        glVertex2f(self.m_p2.x(), self.m_p2.y())
        glEnd()
    
    def setModel(self, model):
        self.m_model = model

    def mousePressEvent(self, event):
        print(event.position())
        self.m_p1 = event.position()

    def mouseMoveEvent(self, event):
        self.m_p2 = event.position()
        self.update()

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


def main():
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()