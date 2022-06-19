import sys
from PyQt5 import QtOpenGL
from PyQt5.QtWidgets import *
from OpenGL.GL import *


class MyCanvas(QtOpenGL.QGLWidget):

    def __init__(self):
        super(MyCanvas, self).__init__()
        self.setGeometry(100, 100, 1200, 800)
        self.setWindowTitle('Drawer')
        self.width = 0
        self.height = 0

    def initializeGL(self):
        glClear(GL_COLOR_BUFFER_BIT)

    def resizeGL(self, width, height):
        self.width = width
        self.height = height
        glViewport(0, 0, self.width, self.height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(0, self.width, 0, self.height, -1, 1)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT)

    def mousePressEvent(self, event):
        pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = MyCanvas()
    widget.show()
    sys.exit(app.exec_())
