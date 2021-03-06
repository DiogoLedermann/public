from PyQt6 import QtOpenGLWidgets, QtCore
from PyQt6.QtWidgets import *
from OpenGL.GL import *

class MyCanvas(QtOpenGLWidgets.QOpenGLWidget):

    def __init__(self):
        super(MyCanvas, self).__init__()
        self.m_model = None
        self.m_w = 0 # width: GL canvas horizontal size
        self.m_h = 0 # height: GL canvas vertical size
        self.m_L = -1000.0
        self.m_R = 1000.0
        self.m_B = -1000.0
        self.m_T = 1000.0
        self.list = None
        self.m_buttonPressed = False
        self.m_pt0 = QtCore.QPoint(0.0,0.0)
        self.m_pt1 = QtCore.QPoint(0.0,0.0)

    def initializeGL(self):
        #glClearColor(1.0, 1.0, 1.0, 1.0)
        glClear(GL_COLOR_BUFFER_BIT)
        # enable smooth line display
        glEnable(GL_LINE_SMOOTH)
        self.list = glGenLists(1)

    def resizeGL(self, _width, _height):
        # store GL canvas sizes in object properties
        self.m_w = _width
        self.m_h = _height
        # Setup world space window limits based on model bounding box
        if (self.m_model == None) or (self.m_model.isEmpty()):
            self.scaleWorldWindow(1.0)
        else:
           self.m_L, self.m_R, self.m_B, self.m_T = self.m_model.getBoundBox()
           self.scaleWorldWindow(1.1)
        # setup the viewport to canvas dimensions
        glViewport(0, 0, self.m_w, self.m_h)
        # reset the coordinate system
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        # establish the clipping volume by setting up an
        # orthographic projection
        #glOrtho(0.0, self.m_w, 0.0, self.m_h, -1.0, 1.0)
        glOrtho(self.m_L, self.m_R, self.m_B, self.m_T, -1.0, 1.0)
        # setup display in model coordinates
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

    def paintGL(self):
        # clear the buffer with the current clear color
        glClear(GL_COLOR_BUFFER_BIT)
        # draw a triangle with RGB color at the 3 vertices
        # interpolating smoothly the color in the interior
        glCallList(self.list)
        glDeleteLists(self.list, 1)
        self.list = glGenLists(1)
        glNewList(self.list, GL_COMPILE)
        # Display model polygon RGB color at its vertices
        # interpolating smoothly the color in the interior
        #glShadeModel(GL_SMOOTH)
        pt0_U = self.convertPtCoordsToUniverse(self.m_pt0)
        pt1_U = self.convertPtCoordsToUniverse(self.m_pt1)
        glColor3f(1.0, 0.0, 0.0)
        glBegin(GL_LINE_STRIP)
        glVertex2f(pt0_U.x(), pt0_U.y())
        glVertex2f(pt1_U.x(), pt1_U.y())
        glEnd()
        if not((self.m_model == None) and (self.m_model.isEmpty())):
            verts = self.m_model.getVerts()
            glColor3f(0.0, 1.0, 0.0) # green
            glBegin(GL_TRIANGLES)
            for vtx in verts:
                glVertex2f(vtx.getX(), vtx.getY())
            glEnd()
            curves = self.m_model.getCurves()
            glColor3f(0.0, 0.0, 1.0) # blue
            glBegin(GL_LINES)
            for curv in curves:
                glVertex2f(curv.getP1().getX(), curv.getP1().getY())
                glVertex2f(curv.getP2().getX(), curv.getP2().getY())
            glEnd()
        glEndList()

    def convertPtCoordsToUniverse(self, _pt):
        dX = self.m_R - self.m_L
        dY = self.m_T - self.m_B
        mX = _pt.x() * dX / self.m_w
        mY = (self.m_h - _pt.y()) * dY / self.m_h
        x = self.m_L + mX
        y = self.m_B + mY
        return QtCore.QPointF(x,y)

    def mousePressEvent(self, event):
        self.m_buttonPressed = True
        self.m_pt0 = event.position()

    def mouseMoveEvent(self, event):
        if self.m_buttonPressed:
            self.m_pt1 = event.position()
            self.update()

    def mouseReleaseEvent(self, event):
        pt0_U = self.convertPtCoordsToUniverse(self.m_pt0)
        pt1_U = self.convertPtCoordsToUniverse(self.m_pt1)
        self.m_model.setCurve(pt0_U.x(),pt0_U.y(),pt1_U.x(),pt1_U.y())
        #self.m_model.setCurve(self.m_pt0.x(),self.m_pt0.y(),self.m_pt1.x(),self.m_pt1.y())
        self.m_buttonPressed = False
        self.m_pt0.setX(0.0)
        self.m_pt0.setY(0.0)
        self.m_pt1.setX(0.0)
        self.m_pt1.setY(0.0)

    def setModel(self,_model):
        self.m_model = _model

    def fitWorldToViewport(self):
        if self.m_model == None:
            return
        self.m_L, self.m_R, self.m_B, self.m_T = self.m_model.getBoundBox()
        self.scaleWorldWindow(1.10)
        self.resizeGL(self.m_w, self.m_h)
        self.update()

    def scaleWorldWindow(self,_scaleFac):
        # Compute canvas viewport distortion ratio.
        vpr = self.m_h / self.m_w
        # Get current window center.
        #/*** COMPLETE HERE - GLCANVAS: 01 ***/
        cx = (self.m_L + self.m_R) / 2.0
        cy = (self.m_B + self.m_T) / 2.0
        #/*** COMPLETE HERE - GLCANVAS: 01 ***/
        # Set new window sizes based on scaling factor.
        #/*** COMPLETE HERE - GLCANVAS: 02 ***/
        sizex = (self.m_R - self.m_L) * _scaleFac
        sizey = (self.m_T - self.m_B) * _scaleFac
        #/*** COMPLETE HERE - GLCANVAS: 02 ***/
        # Adjust window to keep the same aspect ratio of the viewport.
        #/*** COMPLETE HERE - GLCANVAS: 03 ***/
        if sizey > (vpr*sizex):
            sizex = sizey / vpr
        else:
            sizey = sizex * vpr
        self.m_L = cx - (sizex * 0.5)
        self.m_R = cx + (sizex * 0.5)
        self.m_B = cy - (sizey * 0.5)
        self.m_T = cy + (sizey * 0.5)
        #/*** COMPLETE HERE - GLCANVAS: 03 ***/
        # Establish the clipping volume by setting up an
        # orthographic projection
        #glViewport(0, 0, self.m_w, self.m_h)
        #glMatrixMode(GL_PROJECTION) 
        #glLoadIdentity()
        #glOrtho(self.m_L, self.m_R, self.m_B, self.m_T, -1.0, 1.0)
        #glMatrixMode(GL_MODELVIEW)
        #glLoadIdentity()
