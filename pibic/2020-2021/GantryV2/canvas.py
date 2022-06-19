from math import sqrt
from numpy import abs
from PyQt6.QtOpenGLWidgets import QOpenGLWidget
from PyQt6.QtCore import QPoint, Qt
from OpenGL.GL import *
from model import *

class Canvas(QOpenGLWidget):
    
    def __init__(self, parent=None):
        super(Canvas, self).__init__(parent=parent)
        self.parent = parent

        self.width = 0
        self.height = 0
        self.scale = 128
        self.gridSpacing = 64
        self.grid = []
        self.gridCoordinates = []

        self.mode = None

        self.p1 = None
        self.cursorPosition = None
        self.closestNode = None
        self.closestGridPoint = None

        self.model = Model()

    def initializeGL(self):
        glClear(GL_COLOR_BUFFER_BIT)
        glEnable(GL_LINE_SMOOTH)
    
    def resizeGL(self, width, height):
        self.width = width
        self.height = height

        self.setGrid()
        
        glViewport(0, 0, self.width, self.height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(0, self.width, self.height, 0, -1, 1)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT)

        self.paintAxis()
        self.paintGrid()

        if self.closestGridPoint is not None:
            self.paintClosestGridPoint()

        if self.closestNode is not None:
            self.paintClosestNode()
        
        if self.p1 is not None:
            self.paintCurrentElement()

        if len(self.model.elements) > 0:
            self.paintElements()
            
        if len(self.model.nodes) > 0:
            self.paintNodes()
            self.paintRestraints()
            self.paintLoads()

    def paintAxis(self):
        glColor3f(1, 1, 1)
        glBegin(GL_LINE_STRIP)
        glVertex2f(self.scale, 0)
        glVertex2f(self.scale, self.height)
        glEnd()
        glBegin(GL_LINE_STRIP)
        glVertex2f(0, self.height - self.scale)
        glVertex2f(self.width, self.height - self.scale)
        glEnd()

    def paintGrid(self):
        for point in self.grid:
            x, y = point.x(), point.y()
            glColor3f(0, 1, 0)
            glBegin(GL_QUADS)
            glVertex2f(x+2, y+2)
            glVertex2f(x-2, y+2)
            glVertex2f(x-2, y-2)
            glVertex2f(x+2, y-2)
            glEnd()

    def paintClosestGridPoint(self):
        x, y = self.closestGridPoint.x(), self.closestGridPoint.y()
        glColor3f(0, 1, 0)
        glBegin(GL_QUADS)
        glVertex2f(x+5, y+5)
        glVertex2f(x-5, y+5)
        glVertex2f(x-5, y-5)
        glVertex2f(x+5, y-5)
        glEnd()

    def paintClosestNode(self):
        x, y = self.closestNode.x(), self.closestNode.y()
        glColor3f(1, 1, 0)
        glBegin(GL_QUADS)
        glVertex2f(x+5, y+5)
        glVertex2f(x-5, y+5)
        glVertex2f(x-5, y-5)
        glVertex2f(x+5, y-5)
        glEnd()

    def paintCurrentElement(self):
        glColor3f(1, 0, 0)
        glBegin(GL_LINE_STRIP)
        glVertex2f(self.p1.x(), self.p1.y())
        glVertex2f(self.cursorPosition.x(), self.cursorPosition.y())
        glEnd()

    def paintElements(self):
        for i, element in enumerate(self.model.elements):
            node1 = element.n1
            node2 = element.n2

            x1 = (node1.x + 1) * self.scale
            y1 = self.height - ((node1.y + 1) * self.scale)
            x2 = (node2.x + 1) * self.scale
            y2 = self.height - ((node2.y + 1) * self.scale)

            if self.model.brokenElements is None:
                glColor3f(0, 0, 1)
            elif self.model.brokenElements == []:
                glColor3f(0, 1, 0)
            else:
                if self.model.brokenElements[i] is True:
                    glColor3f(1, 0, 0)
                else:
                    glColor3f(0, 0, 1)

            glBegin(GL_LINE_STRIP)
            glVertex2f(x1, y1)
            glVertex2f(x2, y2)
            glEnd()

    def paintNodes(self):
        glColor3f(1, 1, 0)
        for node in self.model.nodes:
            x = (node.x + 1) * self.scale
            y = self.height - ((node.y + 1) * self.scale)
            glBegin(GL_QUADS)
            glVertex2f(x+2, y+2)
            glVertex2f(x-2, y+2)
            glVertex2f(x-2, y-2)
            glVertex2f(x+2, y-2)
            glEnd()
    
    def paintRestraints(self):
        glColor3f(1, 1, 0)
        restraintSize = self.scale / 8
        for node in self.model.nodes:
            x = (node.x + 1) * self.scale
            y = self.height - ((node.y + 1) * self.scale)
            if node.xRestraint is True:
                glBegin(GL_LINE_STRIP)
                glVertex2f(x, y)
                glVertex2f(x - restraintSize, y - restraintSize)
                glVertex2f(x - restraintSize, y + restraintSize)
                glVertex2f(x, y)
                glEnd()
            if node.yRestraint is True:
                glBegin(GL_LINE_STRIP)
                glVertex2f(x, y)
                glVertex2f(x - restraintSize, y + restraintSize)
                glVertex2f(x + restraintSize, y + restraintSize)
                glVertex2f(x, y)
                glEnd()
            if node.momentRestraint is True:
                glBegin(GL_LINE_STRIP)
                glVertex2f(x - restraintSize / 2, y - restraintSize / 2)
                glVertex2f(x + restraintSize / 2, y - restraintSize / 2)
                glVertex2f(x + restraintSize / 2, y + restraintSize / 2)
                glVertex2f(x - restraintSize / 2, y + restraintSize / 2)
                glVertex2f(x - restraintSize / 2, y - restraintSize / 2)
                glEnd()
    
    def paintLoads(self):
        glColor3f(1, 1, 0)
        loadsScale = self.scale / 2
        for node in self.model.nodes:
            x = (node.x + 1) * self.scale
            y = self.height - ((node.y + 1) * self.scale)
            if node.xLoad != 0:
                glBegin(GL_LINE_STRIP)
                glVertex2f(x, y)
                glVertex2f(x + node.xLoad * loadsScale, y)
                glEnd()
                if node.xLoad > 0:
                    glBegin(GL_LINE_STRIP)
                    glVertex2f(x + node.xLoad * loadsScale - loadsScale / 4, y - loadsScale / 4)
                    glVertex2f(x + node.xLoad * loadsScale, y)
                    glVertex2f(x + node.xLoad * loadsScale - loadsScale / 4, y + loadsScale / 4)
                    glEnd()
                else:
                    glBegin(GL_LINE_STRIP)
                    glVertex2f(x + node.xLoad * loadsScale + loadsScale / 4, y - loadsScale / 4)
                    glVertex2f(x + node.xLoad * loadsScale, y)
                    glVertex2f(x + node.xLoad * loadsScale + loadsScale / 4, y + loadsScale / 4)
                    glEnd()
            if node.yLoad != 0:
                glBegin(GL_LINE_STRIP)
                glVertex2f(x, y)
                glVertex2f(x, y - node.yLoad * loadsScale)
                if node.yLoad > 0:
                    glEnd()
                    glBegin(GL_LINE_STRIP)
                    glVertex2f(x - loadsScale / 4, y - node.yLoad * loadsScale + loadsScale / 4)
                    glVertex2f(x, y - node.yLoad * loadsScale)
                    glVertex2f(x + loadsScale / 4, y - node.yLoad * loadsScale  + loadsScale / 4)
                    glEnd()
                else:
                    glEnd()
                    glBegin(GL_LINE_STRIP)
                    glVertex2f(x - loadsScale / 4, y - node.yLoad * loadsScale - loadsScale / 4)
                    glVertex2f(x, y - node.yLoad * loadsScale)
                    glVertex2f(x + loadsScale / 4, y - node.yLoad * loadsScale - loadsScale / 4)
                    glEnd()
            if node.momentRestraint is True:
                pass

    def mousePressEvent(self, event):
        if self.mode == 'Draw':
            if event.button() == Qt.MouseButton.LeftButton:
                if self.p1 is None:

                    if self.closestNode is not None:
                        self.p1 = self.closestNode
                    elif self.closestGridPoint is not None:
                        self.p1 = self.closestGridPoint
                    else:
                        self.p1 = event.position()

                    x = self.p1.x() / self.scale - 1
                    y = (self.height - self.p1.y()) / self.scale - 1
                    node1 = Node(x, y)

                    for node2 in self.model.nodes:
                        if node1 == node2:
                            break
                    else:
                        self.model.addNode(node1)
                    
                    self.update()

                else:
                    x1 = self.p1.x() / self.scale - 1
                    y1 = (self.height - self.p1.y()) / self.scale - 1
                    node1 = Node(x1, y1)

                    if self.closestNode is not None:
                        node2 = self.closestNode
                        self.p1 = self.closestNode
                    elif self.closestGridPoint is not None:
                        node2 = self.closestGridPoint
                        self.p1 = self.closestGridPoint
                    else:
                        node2 = event.position()
                        self.p1 = event.position()
                        
                    x2 = node2.x() / self.scale - 1
                    y2 = (self.height - node2.y()) / self.scale - 1
                    node2 = Node(x2, y2)
                    newElement = Element(node1, node2)

                    for node in self.model.nodes:
                        if node == node2:
                            break
                    else:
                        self.model.addNode(node2)
                    
                    for element in self.model.elements:
                        if element == newElement:
                            break
                    else:
                        self.model.addElement(newElement)

                    self.update()

            elif event.button() == Qt.MouseButton.RightButton:
                self.p1 = None
                self.update()

        elif self.mode == 'Restraints':
            if self.closestNode is not None:
                x = self.closestNode.x() / self.scale - 1
                y = (self.height - self.closestNode.y()) / self.scale - 1
                for node in self.model.nodes:
                    if node.x == x and node.y == y:
                        break
                if event.button() == Qt.MouseButton.LeftButton:
                    if node.xRestraint is False:
                        node.setXRestraint(True)
                    else:
                        node.setXRestraint(False)
                elif event.button() == Qt.MouseButton.RightButton:
                    if node.yRestraint is False:
                        node.setYRestraint(True)
                    else:
                        node.setYRestraint(False)
                elif event.button() == Qt.MouseButton.MiddleButton:
                    if node.momentRestraint is False:
                        node.setMomentRestraint(True)
                    else:
                        node.setMomentRestraint(False)
                self.update()
        
        elif self.mode == 'Loads':
            if self.closestNode is not None:
                x = self.closestNode.x() / self.scale - 1
                y = (self.height - self.closestNode.y()) / self.scale - 1
                for node in self.model.nodes:
                    if node.x == x and node.y == y:
                        break
                if event.button() == Qt.MouseButton.LeftButton:
                    node.setXLoad(self.parent.toolBarDoubleSpinBox.value())
                elif event.button() == Qt.MouseButton.RightButton:
                    node.setYLoad(self.parent.toolBarDoubleSpinBox.value())
                elif event.button() == Qt.MouseButton.MiddleButton:
                    node.setMoment(self.parent.toolBarDoubleSpinBox.value())
                self.update()

    def mouseMoveEvent(self, event):
        self.cursorPosition = event.position()
        tolerance = 5

        self.findClosestGridPoint(tolerance)

        if len(self.model.nodes) > 0:
            self.findClosestNode(tolerance)

        self.update()
    
    def findClosestGridPoint(self, tolerance):
        x1 = self.cursorPosition.x()
        y1 = self.cursorPosition.y()
        p1 = x1, y1
        distances = [sqrt((x1 - x2)**2 + (y1 - y2)**2) for x2, y2 in self.gridCoordinates]

        closest = self.grid[distances.index(min(distances))]

        x2 = closest.x()
        y2 = closest.y()

        if abs(x1 - x2) < tolerance and abs(y1 - y2) < tolerance:
            self.closestGridPoint = closest
        else:
            self.closestGridPoint = None
    
    def findClosestNode(self, tolerance):
        x1 = self.cursorPosition.x()
        y1 = self.cursorPosition.y()
        p1 = x1, y1
        distances = []
        for node in self.model.nodes:
            x2 = (node.x + 1) * self.scale
            y2 = self.height - ((node.y + 1) * self.scale)
            p2 = x2, y2
            distances.append(sqrt((x1 - x2)**2 + (y1 - y2)**2))

        closest = self.model.nodes[distances.index(min(distances))]

        x2 = (closest.x + 1) * self.scale
        y2 = self.height - ((closest.y + 1) * self.scale)

        if abs(x1 - x2) < tolerance and abs(y1 - y2) < tolerance:
            self.closestNode = QPoint(x2, y2)
        else:
            self.closestNode = None

    def setMode(self, mode):
        self.mode = mode

    def setModel(self, model):
        self.model = model
    
    def setScale(self, value):
        self.scale = value
        self.gridSpacing = value
        self.setGrid()

    def setGridSpacing(self, value):
        self.gridSpacing = value
        self.setGrid()

    def setGrid(self):
        xrange = range(self.scale, self.width, self.gridSpacing)
        yrange = range(self.height - self.scale, 0, -self.gridSpacing)
        self.grid = [QPoint(x, y) for x in xrange for y in yrange]
        self.gridCoordinates = [(x, y) for x in xrange for y in yrange]
        self.update()
