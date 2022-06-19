from OpenGL.raw.GL.VERSION.GL_1_0 import GL_QUADS
from PyQt5 import QtCore      # core Qt functionality
from PyQt5 import QtGui       # extends QtCore with GUI functionality
from PyQt5 import QtOpenGL    # provides QGLWidget, a special OpenGL QWidget

from PyQt5 import QtWidgets
from PyQt5.QtOpenGL import *

import OpenGL.GL as gl        # python wrapping of OpenGL
from OpenGL import GLU        # OpenGL Utility Library, extends OpenGL functionality

import sys                    # we'll need this later to run our Qt application

from OpenGL.arrays import vbo
import numpy as np
np.set_printoptions(precision=3, linewidth=np.inf)

class GLWidget(QGLWidget):
    
    def __init__(self, parent=None):
        self.parent = parent
        QtOpenGL.QGLWidget.__init__(self, parent)
            
    def initializeGL(self):
        self.qglClearColor(QtGui.QColor(0, 0, 255))    # initialize the screen to blue
        gl.glEnable(gl.GL_DEPTH_TEST)                  # enable depth testing

        self.rotX = 0.0
        self.rotY = 0.0
        self.rotZ = 0.0

    def resizeGL(self, width, height):
        gl.glViewport(0, 0, width, height)
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()
        aspect = width / float(height)

        GLU.gluPerspective(45.0, aspect, 1.0, 100.0)
        gl.glMatrixMode(gl.GL_MODELVIEW)

    def paintGL(self):
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)

        gl.glPushMatrix()    # push the current matrix to the current stack

        gl.glTranslate(0.0, 0.0, -50.0)    # third, translate cube to specified depth
        gl.glScale(20.0, 20.0, 20.0)       # second, scale cube
        gl.glRotate(self.rotX, 1.0, 0.0, 0.0)
        gl.glRotate(self.rotY, 0.0, 1.0, 0.0)
        gl.glRotate(self.rotZ, 0.0, 0.0, 1.0)
        gl.glTranslate(-0.5, -0.5, -0.5)   # first, translate cube center to origin

        if len(self.parent.quads) > 0:
            for i, quad in enumerate(self.parent.quads):
                r, g, b = self.parent.colors[i]
                
                gl.glColor3f(r, g, b)
                gl.glBegin(gl.GL_QUADS)
                
                for vertex in quad:
                    x, y, z = vertex
                    gl.glVertex3f(x, y, z)
                
                gl.glEnd()

        gl.glPopMatrix()    # restore the previous modelview matrix

    def setRotX(self, val):
        self.rotX = (np.pi * val) / 10

    def setRotY(self, val):
        self.rotY = (np.pi * val) / 10

    def setRotZ(self, val):
        self.rotZ = (np.pi * val) / 10

class MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)    # call the init for the parent class
        
        self.resize(300, 300)
        self.setWindowTitle('Hello OpenGL App')

        self.glWidget = GLWidget(self)
        self.initGUI()

        self.colors = []
        self.quads = []
        
        timer = QtCore.QTimer(self)
        timer.setInterval(20)   # period, in milliseconds
        timer.timeout.connect(self.glWidget.updateGL)
        timer.start()

    def initGUI(self):
        central_widget = QtWidgets.QWidget()
        gui_layout = QtWidgets.QVBoxLayout()
        central_widget.setLayout(gui_layout)

        self.setCentralWidget(central_widget)

        gui_layout.addWidget(self.glWidget)

        sliderX = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        sliderX.setMaximum(1150)
        sliderX.valueChanged.connect(lambda val: self.glWidget.setRotX(val))

        sliderY = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        sliderY.setMaximum(1145)
        sliderY.valueChanged.connect(lambda val: self.glWidget.setRotY(val))

        sliderZ = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        sliderZ.setMaximum(1145)
        sliderZ.valueChanged.connect(lambda val: self.glWidget.setRotZ(val))
        
        gui_layout.addWidget(sliderX)
        gui_layout.addWidget(sliderY)
        gui_layout.addWidget(sliderZ)

    def getQuadModel(self, i, pivot, deltas):
        h, v = pivot
        dh, dv = deltas

        models = [
            [
                [0, h,      v     ],
                [0, h + dh, v     ],
                [0, h + dh, v + dv],
                [0, h,      v + dv]
            ],
            [
                [1, h,      v     ],
                [1, h + dh, v     ],
                [1, h + dh, v + dv],
                [1, h,      v + dv]
            ],
            [
                [h,      0, v     ],
                [h + dh, 0, v     ],
                [h + dh, 0, v + dv],
                [h,      0, v + dv]
            ],
            [
                [h,      1, v     ],
                [h + dh, 1, v     ],
                [h + dh, 1, v + dv],
                [h,      1, v + dv]
            ],
            [
                [h,      v     , 0],
                [h + dh, v     , 0],
                [h + dh, v + dv, 0],
                [h,      v + dv, 0]
            ],
            [
                [h,      v     , 1],
                [h + dh, v     , 1],
                [h + dh, v + dv, 1],
                [h,      v + dv, 1]
            ],
        ]

        return models[i]

    def setData(self):
        # # initialize the main image data
        # self.m_data = None # numpy array
        # self.m_image = None # QImage object
        # self.m_map = []  # path of all image files 
        # self.dataset = None
        # # check if there is at least one image open, and then proceed:
        # if len(self.m_map) == 0:
        #     return
        # loadedFirst = False
        # for filepath in self.m_map:
        #     self.loadImageData(filepath,False)
        #     self.m_data[self.m_data>0] = 1
        #     self.m_data = 1-self.m_data
        #     if loadedFirst:
        #         dataset = np.vstack([dataset, self.m_data[np.newaxis,...]])
        #     else:
        #         loadedFirst = True
        #         dataset = self.m_data[np.newaxis,...]

        # print(f'Tomo size: {len(dataset)}')
        
        imgXi = [
            [0, 1, 1],
            [0, 0, 0],
            [0, 0, 1],
        ]
        imgXf = [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
        ]
        imgYi = [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
        ]
        imgYf = [
            [1, 0, 0],
            [0, 0, 0],
            [1, 0, 0],
        ]
        imgZi = [
            [0, 0, 0],
            [1, 0, 0],
            [1, 0, 0],
        ]
        imgZf = [
            [0, 0, 0],
            [0, 0, 0],
            [1, 0, 0],
        ]

        faces = imgXi, imgXf, imgYi, imgYf, imgZi, imgZf

        for i, face in enumerate(faces):
            hLen = len(face[0])
            vLen = len(face)

            deltas = 1 / hLen, 1 / vLen

            for r in range(vLen):
                for c in range(hLen):

                    if face[r][c] == 0:
                        self.colors.append([1.0, 1.0, 1.0])
                    elif face[r][c] == 1:
                        self.colors.append([0.0, 0.0, 0.0])

                    pivot = c / hLen, r / vLen

                    quad = self.getQuadModel(i, pivot, deltas)

                    self.quads.append(quad)
        
if __name__ == '__main__':

    app = QtWidgets.QApplication(sys.argv)
    
    win = MainWindow()
    win.setData()
    win.show()

    sys.exit(app.exec_())
