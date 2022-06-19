"""
A simple GUI that allows to load and visualize a stack of images (slices)
from micro-computed tomography converted to 2D (or 3D) Numpy arrays.
Basic current capabilities:
- Visualize the image stack;
- Plot image histogram;
- Resample the data;
- Export to RAW (JSON) format;
- Identify unconnected pores;
- Replicate a single image;
"""

import os
import sys
import json
import numpy as np
import matplotlib as mpl
from matplotlib.backends.backend_qt5agg import (FigureCanvasQTAgg, NavigationToolbar2QT)
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from PyQt5 import QtCore, QtGui, QtWidgets 
from time import perf_counter
from hetool import *

ORGANIZATION_NAME = 'LCC-IC-UFF'
ORGANIZATION_DOMAIN = 'www.ic.uff.br/~andre/'
APPLICATION_NAME = 'pyTomoViewer'
SETTINGS_TRAY = 'settings/tray'

# Inherit from QDialog
#class TomoViewer(QtWidgets.QDialog):
class TomoViewer(QtWidgets.QMainWindow):
    # Override the class constructor
    def __init__(self, parent=None):
        super(TomoViewer, self).__init__(parent)
        # setting main Widget 
        self.main = QtWidgets.QWidget()
        self.setCentralWidget(self.main)        
        # setting title 
        self.setWindowTitle(APPLICATION_NAME) 
        # setting geometry and minimum size
        self.setGeometry(100, 100, 600, 600) 
        self.setMinimumSize(QtCore.QSize(400, 400))
        # a figure instance to plot on
        self.figure = Figure()
        # this is the Canvas widget that displays the 'figure'
        self.canvas = FigureCanvasQTAgg(self.figure)
        mpl.rcParams['image.cmap'] = 'gray' # magma, seismic
        # this is the Navigation widget
        self.toolbar = NavigationToolbar2QT(self.canvas, self)
        # this is the Menu bar 
        bar = self.menuBar()
        mfile = bar.addMenu("&File")
        open_action = QtWidgets.QAction("&Open...", self)
        open_action.setShortcut('Ctrl+O')
        open_action.triggered.connect(self.openImage)
        save_action = QtWidgets.QAction("&Export...", self)
        save_action.triggered.connect(self.exportImage)
        exit_action = QtWidgets.QAction("&Exit", self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.triggered.connect(QtWidgets.qApp.quit)
        mfile.addAction(open_action)
        mfile.addAction(save_action)
        mfile.addAction(exit_action)
        mcomp = bar.addMenu("&Compute")
        replc_action = QtWidgets.QAction("&Replicate Image...", self)
        replc_action.triggered.connect(self.replicateImage)
        binar_action = QtWidgets.QAction("&Convert to Binary Image...", self)
        binar_action.setShortcut('Ctrl+B')
        binar_action.triggered.connect(self.convertToBinary)
        saveIFC_action = QtWidgets.QAction("&Save IFC...", self)
        saveIFC_action.setShortcut('Ctrl+S')
        saveIFC_action.triggered.connect(self.saveIFC)
        createModels_action = QtWidgets.QAction("&Create Models...", self)
        createModels_action.setShortcut('Ctrl+C')
        createModels_action.triggered.connect(self.enumerateRegions)
        mcomp.addAction(replc_action)
        mcomp.addAction(binar_action)
        mcomp.addAction(saveIFC_action)
        mcomp.addAction(createModels_action)
        mhelp = bar.addMenu("&Help")
        about_action = QtWidgets.QAction("&About...", self)
        about_action.triggered.connect(self.aboutDlg)
        mhelp.addAction(about_action)
        # these are the app widgets connected to their slot methods
        self.slideBar = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.slideBar.setMinimum(0)
        self.slideBar.setTickPosition(QtWidgets.QSlider.TicksBothSides)
        self.slideBar.setTickInterval(1)        
        self.slideBar.setSingleStep(1)
        self.slideBar.setEnabled(False)
        self.slideBar.valueChanged[int].connect(self.changeValue)
        self.buttonPlus = QtWidgets.QPushButton('+')
        self.buttonPlus.setMaximumSize(QtCore.QSize(25, 30))
        self.buttonPlus.setEnabled(False)
        self.buttonPlus.clicked.connect(self.slideMoveUp)
        self.buttonMinus = QtWidgets.QPushButton('-')
        self.buttonMinus.setMaximumSize(QtCore.QSize(25, 30))
        self.buttonMinus.setEnabled(False) 
        self.buttonMinus.clicked.connect(self.slideMoveDown)        
        self.buttonPlot = QtWidgets.QPushButton('View Image')
        self.buttonPlot.setEnabled(False)
        self.buttonPlot.clicked.connect(self.plotImage)       
        self.buttonHist = QtWidgets.QPushButton('View Histogram')
        self.buttonHist.setEnabled(False)
        self.buttonHist.clicked.connect(self.plotHistogram)
        self.labelDimensions = QtWidgets.QLabel('[h=0,w=0]')
        self.labelSliceId = QtWidgets.QLabel('Slice = 0')
        self.labelSliceId.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        # set the layouts
        mainLayout = QtWidgets.QVBoxLayout(self.main)
        mainLayout.addWidget(self.toolbar)
        layoutH2 = QtWidgets.QHBoxLayout()
        layoutH3 = QtWidgets.QHBoxLayout()
        layoutH2.addWidget(self.buttonMinus)        
        layoutH2.addWidget(self.slideBar)        
        layoutH2.addWidget(self.buttonPlus)  
        layoutH3.addWidget(self.buttonPlot)
        layoutH3.addWidget(self.buttonHist)
        layoutH3.addWidget(self.labelDimensions)
        layoutH3.addItem(QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.MinimumExpanding))
        layoutH3.addWidget(self.labelSliceId)
        mainLayout.addWidget(self.canvas, QtWidgets.QSizePolicy.MinimumExpanding)
        mainLayout.addLayout(layoutH2)
        mainLayout.addLayout(layoutH3)           
        # initialize the main image data
        self.m_data = None # numpy array
        self.m_image = None # QImage object
        self.m_map = []  # path of all image files 
        self.dataset = None

    def __del__(self):
        # remove temporary data: 
        self.m_data = None
        self.m_image = None
        if len(self.m_map) > 0:
            self.removeTempImagens()

    # @Slot()
    def plotImage(self):
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        img = ax.imshow(self.m_data,vmin=0,vmax=255)      
        self.figure.colorbar(img)
        ax.figure.canvas.draw()
        self.buttonPlot.setEnabled(False)          
        self.buttonHist.setEnabled(True)        

    # @Slot()
    def plotHistogram(self):
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.hist(self.m_data.flatten(), bins=256, fc='k', ec='k')
        ax.set(xlim=(-4, 259))
        ax.figure.canvas.draw()
        self.buttonPlot.setEnabled(True)          
        self.buttonHist.setEnabled(False)   

    # @Slot()
    def changeValue(self, _value):
        filename = self.m_map[_value]
        self.loadImageData(filename,True)
        self.labelSliceId.setText("Slice = "+str(_value+1))

    # @Slot()
    def slideMoveUp(self):
        self.slideBar.setValue(self.slideBar.value()+1)

    # @Slot()
    def slideMoveDown(self):
        self.slideBar.setValue(self.slideBar.value()-1)

    # @Slot()
    def openImage(self):
        options = QtWidgets.QFileDialog.Options()
        files, _ = QtWidgets.QFileDialog.getOpenFileNames(self,"Open Tomo", "","Image Files (*.tif);;Image Files (*.tiff)", options=options)
        if files:
            if len(self.m_map) > 0:
                self.removeTempImagens()
            self.m_map.clear() # remove all items
            for filepath in files:
                self.m_map.append( filepath )
            self.loadImageData(files[0],True)
            self.buttonPlus.setEnabled(True) 
            self.buttonMinus.setEnabled(True) 
            self.slideBar.setMaximum(len(self.m_map)-1)
            self.slideBar.setValue(0)
            self.slideBar.setEnabled(True)
            self.labelSliceId.setText("Slice = 1")

    # @Slot()
    def exportImage(self):
        # check if there is at least one image open, and then proceed:
        if len(self.m_map) == 0:
            return
        options = QtWidgets.QFileDialog.Options()
        filename = QtWidgets.QFileDialog.getSaveFileName(self, 'Save Image Data', '', "Raw Files (*.raw);;Image Files (*.tif)", options=options)
        if filename[1] == 'Raw Files (*.raw)':
            if filename[0][-4:] != '.raw':
                filename = filename[0] + '.raw'
            else:
                filename = filename[0] 
            materials = {} 
            # Save image data in RAW format
            with open(filename, "bw") as file_raw:
                for filepath in self.m_map:
                    self.loadImageData(filepath,False)
                    mat_i, cmat_i = np.unique(self.m_data,return_counts=True)
                    for i in range(len(mat_i)):
                        if mat_i[i] in materials:  
                            materials[mat_i[i]] += cmat_i[i]
                        else:
                            materials[mat_i[i]] = cmat_i[i]
                    # Save image data in binary format
                    self.m_data.tofile(file_raw) 
            self.loadImageData(self.m_map[self.slideBar.value()],True)
            materials = dict(sorted(materials.items(), key=lambda x: x[0]))
            dimensions = np.array([self.m_data.shape[1],self.m_data.shape[0],len(self.m_map)],dtype=int)
            vol = self.m_data.shape[1]*self.m_data.shape[0]*len(self.m_map)
            mat = np.array(list(materials.keys()))  
            cmat = np.array(list(materials.values()))   
            mat = np.vstack((mat, np.zeros((mat.shape[0]),dtype=int))).T
            cmat = cmat*100.0/vol      
            jdata = {}
            jdata["type_of_analysis"] = 0
            jdata["type_of_solver"] = 0
            jdata["type_of_rhs"] = 0
            jdata["voxel_size"] = 1.0
            jdata["solver_tolerance"] = 1.0e-6
            jdata["number_of_iterations"] = 1000
            jdata["image_dimensions"] = dimensions.tolist()          
            jdata["refinement"] = 1
            jdata["number_of_materials"] = mat.shape[0]
            jdata["properties_of_materials"] = mat.tolist()
            jdata["volume_fraction"] = list(np.around(cmat,2))
            jdata["data_type"] = "uint8"
            # Save image data in JSON format
            with open(filename[0:len(filename)-4] + ".json",'w') as file_json:
                json.dump(jdata,file_json,sort_keys=False, indent=4, separators=(',', ': '))
            # Save image data in NF format
            with open(filename[0:len(filename)-4] + ".nf",'w') as file_nf:
                sText = ''
                for k, v in jdata.items():
                    sText += '%' + str(k) + '\n'+ str(v) + '\n\n'
                sText = sText.replace('], ','\n')
                sText = sText.replace('[','')
                sText = sText.replace(']','')
                sText = sText.replace(',','')
                file_nf.write(sText)
        elif filename[1] == 'Image Files (*.tif)' and filename[0][-4:] == '.tif':
            refine, ok = QtWidgets.QInputDialog.getInt(self,"Resampling","Refinement level:", 1, 1, 100, 1)
            if ok:
                filename = filename[0]
                i = 0
                for filepath in self.m_map:
                    self.loadImageData(filepath,False)
                    h = self.m_data.shape[0]
                    w = self.m_data.shape[1]
                    for _ in range(refine):
                        i += 1
                        imgNumber = '{:04d}'.format(i)
                        # Save image data in TIF format
                        self.m_image.scaled(refine*h, refine*w).save(filename[:-4]+"_"+imgNumber+".tif")
                self.loadImageData(self.m_map[self.slideBar.value()], True)

    # @Slot()
    def replicateImage(self):
        # check if there is at least one image open, and then proceed:
        if len(self.m_map) == 0:
            return
        slices, ok = QtWidgets.QInputDialog.getInt(self,"Replicate","Number of slices:", 1, 1, 2024, 1)
        if ok:
            filepath = self.m_map[0]
            self.m_map.clear() # remove all items
            for _ in range(slices):
                self.m_map.append( filepath )
            self.loadImageData(filepath,True)
            self.buttonPlus.setEnabled(True) 
            self.buttonMinus.setEnabled(True) 
            self.slideBar.setMaximum(len(self.m_map)-1)
            self.slideBar.setValue(0)
            self.slideBar.setEnabled(True)
            self.labelSliceId.setText("Slice = 1")

    # @Slot()
    def convertToBinary(self):
        # check if there is at least one image open, and then proceed:
        if len(self.m_map) == 0:
            return
        threshold, ok = QtWidgets.QInputDialog.getInt(self,"Convert image to binary image","Threshold:", 1, 1, 256, 1)
        if ok:
            nImg = len(self.m_map)
            for i in range(nImg):
                self.loadImageData(self.m_map[i],False)
                self.m_data[self.m_data>=threshold] = 255
                self.m_data[self.m_data<threshold]  = 0
                im = np.uint8(self.m_data)
                im = np.uint8(self.m_data)
                bytesPerLine = im.shape[1]
                image = QtGui.QImage(im, im.shape[1], im.shape[0], bytesPerLine, QtGui.QImage.Format_Grayscale8)
                imgNumber = '{:04d}'.format(i)
                filepath = "temp_image_"+imgNumber+".tif"
                image.save(filepath)
                self.m_map[i] = filepath 
            self.loadImageData(self.m_map[self.slideBar.value()], True)

    # @Slot()
    def aboutDlg(self):
        sm = """pyTomoViewer\nVersion 1.0.0\n2020\nLicense GPL 3.0\n\nThe authors and the involved Institutions are not responsible for the use or bad use of the program and their results. The authors have no legal dulty or responsability for any person or company for the direct or indirect damage caused resulting from the use of any information or usage of the program available here. The user is responsible for all and any conclusion made with the program. There is no warranty for the program use. """
        msg = QtWidgets.QMessageBox()
        msg.setText(sm)
        msg.setWindowTitle("About")
        msg.exec_()

    # @Slot()
    def saveIFC(self):
        # check if there is at least one image open, and then proceed:
        if len(self.m_map) == 0:
            return
        loadedFirst = False
        for filepath in self.m_map:
            self.loadImageData(filepath,False)
            self.m_data[self.m_data>0] = 1
            self.m_data = 1-self.m_data
            if loadedFirst:
                dataset = np.vstack([dataset, self.m_data[np.newaxis,...]])
            else:
                loadedFirst = True
                dataset = self.m_data[np.newaxis,...]

        print(f'Tomo size: {len(dataset)}')
        
        imgXi = dataset[:,:,0]
        imgXf = dataset[:,:,-1]
        imgYi = dataset[:,0]
        imgYf = dataset[:,-1]
        imgZi = dataset[0]
        imgZf = dataset[-1]

        faces = imgXi, imgXf, imgYi, imgYf, imgZi, imgZf

        xMax = len(dataset[0][0])
        yMax = len(dataset[0])
        zMax = len(dataset)

        externalTriangles1 = [
            [],
            [],
            [],
            [],
            [],
            []
        ]
        externalTriangles2 = [
            [],
            [],
            [],
            [],
            [],
            []
        ]
        externalCoords = [
            [],
            [],
            [],
            [],
            [],
            []
        ]
        internalTriangles1 = [
            [],
            [],
            []
        ]
        internalTriangles2 = [
            [],
            [],
            []
        ]
        internalCoords = [
            [],
            [],
            []
        ]

        ti = perf_counter()
        for i, face in enumerate(faces):
            nRows = len(face)
            nCols = len(face[0])

            idArray = [i + 1 for i in range((nRows + 1) * (nCols + 1))]
            idArray = np.reshape(idArray, ((nRows + 1), (nCols + 1)))

            for r in range(nRows):
                for c in range(nCols):
                    if face[r][c] == 0:
                        externalTriangles1[i].append((idArray[r][c], idArray[r][c+1], idArray[r+1][c+1]))
                        externalTriangles1[i].append((idArray[r][c], idArray[r+1][c], idArray[r+1][c+1]))
                    elif face[r][c] == 1:
                        externalTriangles2[i].append((idArray[r][c], idArray[r][c+1], idArray[r+1][c+1]))
                        externalTriangles2[i].append((idArray[r][c], idArray[r+1][c], idArray[r+1][c+1]))

            if i == 0:
                for z in range(nRows + 1):
                    for y in range(nCols + 1):
                        externalCoords[i].append((0, y, z))

            elif i == 1:
                for z in range(nRows + 1):
                    for y in range(nCols + 1):
                        externalCoords[i].append((xMax, y, z))

            elif i == 2:
                for z in range(nRows + 1):
                    for x in range(nCols + 1):
                        externalCoords[i].append((x, 0, z))

            elif i == 3:
                for z in range(nRows + 1):
                    for x in range(nCols + 1):
                        externalCoords[i].append((x, yMax, z))
            
            elif i == 4:
                for y in range(nRows + 1):
                    for x in range(nCols + 1):
                        externalCoords[i].append((x, y, 0))

            elif i == 5:
                for y in range(nRows + 1):
                    for x in range(nCols + 1):
                        externalCoords[i].append((x, y, zMax))
        print(f'External triangles: {perf_counter() - ti}')

        ti = perf_counter()
        n = 0
        for i in range(zMax - 1):
            nRows = len(dataset[i])
            nCols = len(dataset[i][0])
            for r in range(nRows):
                for c in range(nCols):
                    if dataset[i][r][c] != dataset[i+1][r][c]:
                        internalTriangles1[0].append((n*4+1, n*4+2, n*4+3))
                        internalTriangles1[0].append((n*4+3, n*4+4, n*4+1))
                        internalTriangles2[0].append((n*4+1, n*4+2, n*4+3))
                        internalTriangles2[0].append((n*4+3, n*4+4, n*4+1))
                        internalCoords[0].append((c, r, i+1))
                        internalCoords[0].append((c+1, r, i+1))
                        internalCoords[0].append((c+1, r+1, i+1))
                        internalCoords[0].append((c, r+1, i+1))
                        n += 1
        
        n = 0
        for i in range(yMax - 1):
            nRows = len(dataset[:,i])
            nCols = len(dataset[:,i][0])
            for r in range(nRows):
                for c in range(nCols):
                    if dataset[:,i][r][c] != dataset[:,i+1][r][c]:
                        internalTriangles1[1].append((n*4+1, n*4+2, n*4+3))
                        internalTriangles1[1].append((n*4+3, n*4+4, n*4+1))
                        internalTriangles2[1].append((n*4+1, n*4+2, n*4+3))
                        internalTriangles2[1].append((n*4+3, n*4+4, n*4+1))
                        internalCoords[1].append((c, i+1, r))
                        internalCoords[1].append((c+1, i+1, r))
                        internalCoords[1].append((c+1, i+1, r+1))
                        internalCoords[1].append((c, i+1, r+1))
                        n += 1
        
        n = 0
        for i in range(xMax - 1):
            nRows = len(dataset[:,:,i])
            nCols = len(dataset[:,:,i][0])
            for r in range(nRows):
                for c in range(nCols):
                    if dataset[:,:,i][r][c] != dataset[:,:,i+1][r][c]:
                        internalTriangles1[2].append((n*4+1, n*4+2, n*4+3))
                        internalTriangles1[2].append((n*4+3, n*4+4, n*4+1))
                        internalTriangles2[2].append((n*4+1, n*4+2, n*4+3))
                        internalTriangles2[2].append((n*4+3, n*4+4, n*4+1))
                        internalCoords[2].append((i+1, c, r))
                        internalCoords[2].append((i+1, c+1, r))
                        internalCoords[2].append((i+1, c+1, r+1))
                        internalCoords[2].append((i+1, c, r+1))
                        n += 1
        print(f'Internal triangles: {perf_counter() - ti}')

        ti = perf_counter()
        with open(f'outFile.ifc', 'w') as outFile:
            outFile.write(
                "ISO-10303-21;\n"
                "HEADER;\n"
                "FILE_DESCRIPTION( ( 'ViewDefinition "
                    + "[notYetAssigned]' ,'Comment [manual "
                    + "creation of example file]' ) ,'2;1');\n"
                "FILE_NAME( 'IfcBuildingElementProxy_Tessellation.ifc', "
                    + "'2012-07-04T18:00:00', ('Thomas Liebich'), "
                    + "('buildingSMART International'), 'IFC text editor', "
                    + "'IFC text editor', 'reference file created for the "
                    + "IFC4 specification');\n"
                "FILE_SCHEMA(('IFC4'));\n"
                "ENDSEC;\n"
                "DATA;\n"
                "#100= IFCPROJECT ('0xScRe4drECQ4DMSqUjd6d',#110,'proxy with "
                    + "tessellation',$,$,$,$,(#201),#301);\n"
                "#110= IFCOWNERHISTORY (#111,#115,$,.ADDED.,1320688800,$,$, "
                    + "1320688800);\n"
                "#111= IFCPERSONANDORGANIZATION (#112,#113,$);\n"
                "#112= IFCPERSON ($,'Liebich','Thomas',$,$,$,$,$);\n"
                "#113= IFCORGANIZATION ($,'buildingSMART International', "
                    + "$,$,$);\n"
                "#115= IFCAPPLICATION (#113,'1.0','IFC text editor', "
                    + "'ifcTE');\n"
                "#201= IFCGEOMETRICREPRESENTATIONCONTEXT ($,'Model',3,1.0E-5, "
                    + "#210,$);\n"
                "#202= IFCGEOMETRICREPRESENTATIONSUBCONTEXT ('Body','Model', "
                    + "*,*,*,*,#201,$,.MODEL_VIEW.,$);\n"
                "#210= IFCAXIS2PLACEMENT3D (#901,$,$);\n"
                "#301= IFCUNITASSIGNMENT ((#311,#312));\n"
                "#311= IFCSIUNIT (*,.LENGTHUNIT.,.MILLI.,.METRE.);\n"
                "#312= IFCCONVERSIONBASEDUNIT (#313,.PLANEANGLEUNIT., "
                    + "'degree',#314);\n"
                "#313= IFCDIMENSIONALEXPONENTS (0,0,0,0,0,0,0);\n"
                "#314= IFCMEASUREWITHUNIT (IFCPLANEANGLEMEASURE(0.017453293), "
                    + "#315);\n"
                "#315= IFCSIUNIT (*,.PLANEANGLEUNIT.,$,.RADIAN.);\n"
                "#500= IFCBUILDING ('2FCZDorxHDT8NI01kdXi8P',$,'Test "
                    + "Building',$,$,#511,$,$,.ELEMENT.,$,$,$);\n"
                "#511= IFCLOCALPLACEMENT ($,#512);\n"
                "#512= IFCAXIS2PLACEMENT3D (#901,$,$);\n"
                "#519= IFCRELAGGREGATES ('2YBqaV_8L15eWJ9DA1sGmT',$,$,$,#100, "
                    + "(#500));\n"
                "#901= IFCCARTESIANPOINT ((0.,0.,0.));\n"
                "#902= IFCDIRECTION ((1.,0.,0.));\n"
                "#903= IFCDIRECTION ((0.,1.,0.));\n"
                "#904= IFCDIRECTION ((0.,0.,1.));\n"
                "#905= IFCDIRECTION ((-1.,0.,0.));\n"
                "#906= IFCDIRECTION ((0.,-1.,0.));\n"
                "#907= IFCDIRECTION ((0.,0.,-1.));\n"

                "#1000= IFCBUILDINGELEMENTPROXY ('1kTvXnbbzCWw8lcMd1dR4o',$, "
                    + "'P-1','sample proxy',$,#9001,#1100,$,$);\n"
                "#2000= IFCBUILDINGELEMENTPROXY ('1kTvXnbbzCWw8lcMd1dR4o',$, "
                    + "'P-1','sample proxy',$,#9001,#2100,$,$);\n"

                "#1100= IFCPRODUCTDEFINITIONSHAPE ($,$,(#1110));\n"
                "#1110= IFCSHAPEREPRESENTATION (#202,'Body'," +
                    "'Tessellation',(#1111, #1112, #1113, #1114, #1115, #1116, #1117, #1118, #1119));\n"

                "#1111= IFCTRIANGULATEDFACESET "
                + f"(#3001,$,.T.,({str(externalTriangles1[0]).strip('[]')}),$);\n"
                
                "#1112= IFCTRIANGULATEDFACESET "
                + f"(#3002,$,.T.,({str(externalTriangles1[1]).strip('[]')}),$);\n"

                "#1113= IFCTRIANGULATEDFACESET "
                + f"(#3003,$,.T.,({str(externalTriangles1[2]).strip('[]')}),$);\n"

                "#1114= IFCTRIANGULATEDFACESET "
                + f"(#3004,$,.T.,({str(externalTriangles1[3]).strip('[]')}),$);\n"

                "#1115= IFCTRIANGULATEDFACESET "
                + f"(#3005,$,.T.,({str(externalTriangles1[4]).strip('[]')}),$);\n"

                "#1116= IFCTRIANGULATEDFACESET "
                + f"(#3006,$,.T.,({str(externalTriangles1[5]).strip('[]')}),$);\n"

                "#1117= IFCTRIANGULATEDFACESET "
                + f"(#3007,$,.T.,({str(internalTriangles1[0]).strip('[]')}),$);\n"

                "#1118= IFCTRIANGULATEDFACESET "
                + f"(#3008,$,.T.,({str(internalTriangles1[1]).strip('[]')}),$);\n"

                "#1119= IFCTRIANGULATEDFACESET "
                + f"(#3009,$,.T.,({str(internalTriangles1[2]).strip('[]')}),$);\n"

                "#2100= IFCPRODUCTDEFINITIONSHAPE ($,$,(#2110));\n"
                "#2110= IFCSHAPEREPRESENTATION (#202,'Body'," +
                    "'Tessellation',(#2111, #2112, #2113, #2114, #2115, #2116, #2117, #2118, #2119));\n"

                "#2111= IFCTRIANGULATEDFACESET "
                + f"(#3001,$,.T.,({str(externalTriangles2[0]).strip('[]')}),$);\n"

                "#2112= IFCTRIANGULATEDFACESET "
                + f"(#3002,$,.T.,({str(externalTriangles2[1]).strip('[]')}),$);\n"

                "#2113= IFCTRIANGULATEDFACESET "
                + f"(#3003,$,.T.,({str(externalTriangles2[2]).strip('[]')}),$);\n"
                
                "#2114= IFCTRIANGULATEDFACESET "
                + f"(#3004,$,.T.,({str(externalTriangles2[3]).strip('[]')}),$);\n"

                "#2115= IFCTRIANGULATEDFACESET "
                + f"(#3005,$,.T.,({str(externalTriangles2[4]).strip('[]')}),$);\n"
                
                "#2116= IFCTRIANGULATEDFACESET "
                + f"(#3006,$,.T.,({str(externalTriangles2[5]).strip('[]')}),$);\n"

                "#2117= IFCTRIANGULATEDFACESET "
                + f"(#3007,$,.T.,({str(internalTriangles2[0]).strip('[]')}),$);\n"

                "#2118= IFCTRIANGULATEDFACESET "
                + f"(#3008,$,.T.,({str(internalTriangles2[1]).strip('[]')}),$);\n"

                "#2119= IFCTRIANGULATEDFACESET "
                + f"(#3009,$,.T.,({str(internalTriangles2[2]).strip('[]')}),$);\n"

                f"#3001= IFCCARTESIANPOINTLIST3D (({str(externalCoords[0]).strip('[]')}));\n"
                f"#3002= IFCCARTESIANPOINTLIST3D (({str(externalCoords[1]).strip('[]')}));\n"
                f"#3003= IFCCARTESIANPOINTLIST3D (({str(externalCoords[2]).strip('[]')}));\n"
                f"#3004= IFCCARTESIANPOINTLIST3D (({str(externalCoords[3]).strip('[]')}));\n"
                f"#3005= IFCCARTESIANPOINTLIST3D (({str(externalCoords[4]).strip('[]')}));\n"
                f"#3006= IFCCARTESIANPOINTLIST3D (({str(externalCoords[5]).strip('[]')}));\n"
                f"#3007= IFCCARTESIANPOINTLIST3D (({str(internalCoords[0]).strip('[]')}));\n"
                f"#3008= IFCCARTESIANPOINTLIST3D (({str(internalCoords[1]).strip('[]')}));\n"
                f"#3009= IFCCARTESIANPOINTLIST3D (({str(internalCoords[2]).strip('[]')}));\n"
                
                "#9001= IFCLOCALPLACEMENT (#511,#9002);\n"
                "#9002= IFCAXIS2PLACEMENT3D (#9003,$,$);\n"
                "#9003= IFCCARTESIANPOINT ((1000.,0.,0.));\n"

                "#10000= IFCRELCONTAINEDINSPATIALSTRUCTURE "
                + "('2TnxZkTXT08eDuMuhUUFNy',$,'Physical model',$,(#1000, #2000), "
                + "#500);\n"

                "ENDSEC;\n"
                "END-ISO-10303-21;")
        print(f'File writing: {perf_counter() - ti}')

        print('Done')

        print()

    # @Slot()
    def enumerateRegions(self):
        # check if there is at least one image open, and then proceed:
        if len(self.m_map) == 0:
            return
        loadedFirst = False
        for filepath in self.m_map:
            self.loadImageData(filepath,False)
            self.m_data[self.m_data>0] = 1
            self.m_data = 1-self.m_data
            if loadedFirst:
                dataset = np.vstack([dataset, self.m_data[np.newaxis,...]])
            else:
                loadedFirst = True
                dataset = self.m_data[np.newaxis,...]

        ti = perf_counter()
        
        models = [
            [],
            []
        ]
        controllers = [
            [],
            []
        ]
        viewers = [
            [],
            [],
        ]
        for i, data in enumerate(dataset):
            print(f'Creating model {i+1}')
            model0 = HeModel()
            model1 = HeModel()
            controller0 = HeController(model0)
            controller1 = HeController(model1)
            viewer0 = HeView(model0)
            viewer1 = HeView(model1)
            
            nRows = len(data)
            nCols = len(data[0])

            for r in range(nRows):
                pt1 = Point(0, r)
                pt2 = Point(0, r+1)
                line = Line(pt1, pt2)
                if data[r][0] == 0:
                    controller0.addSegment(line, 0)
                elif data[r][0] == 1:
                    controller1.addSegment(line, 0)

                for c in range(nCols-1):
                    pt1 = Point(c+1, r)
                    pt2 = Point(c+1, r+1)
                    line = Line(pt1, pt2)
                    if data[r][c] != data[r][c+1]:
                        controller0.addSegment(line, 0)
                        controller1.addSegment(line, 0)

                pt1 = Point(nCols, r)
                pt2 = Point(nCols, r+1)
                line = Line(pt1, pt2)
                if data[r][-1] == 0:
                    controller0.addSegment(line, 0)
                if data[r][-1] == 1:
                    controller1.addSegment(line, 0)

            for c in range(nCols):
                pt1 = Point(c, 0)
                pt2 = Point(c+1, 0)
                line = Line(pt1, pt2)
                if data[0][c] == 0:
                    controller0.addSegment(line, 0)
                elif data[0][c] == 1:
                    controller1.addSegment(line, 0)

                for r in range(nRows-1):
                    pt1 = Point(c, r+1)
                    pt2 = Point(c+1, r+1)
                    line = Line(pt1, pt2)
                    if data[r][c] != data[r+1][c]:
                        controller0.addSegment(line, 0)
                        controller1.addSegment(line, 0)

                pt1 = Point(c, nRows)
                pt2 = Point(c+1, nRows)
                line = Line(pt1, pt2)
                if data[-1][c] == 1:
                    controller0.addSegment(line, 0)
                if data[-1][c] == 1:
                    controller1.addSegment(line, 0)

            models[0].append(model0)
            models[1].append(model1)
            controllers[0].append(controller0)
            controllers[1].append(controller1)
            viewers[0].append(viewer0)
            viewers[1].append(viewer1)

        tf = perf_counter()

        print(f'Models created in {tf - ti:.5f} seconds.')

        ti = perf_counter()

        for i, model in enumerate(models):
            for j, patch in enumerate(model.getPatches()):
                patch.setId((i+1, j+1))
                for segment in patch.segments:
                    segment.setParentId((i+1, j+1))

        tf = perf_counter()

        print(f'Id settings done in {tf - ti:.5f} seconds.')

        ti = perf_counter()

        interModels = []
        interControllers = []
        interViewers = []
        for i in range(len(models) - 1):
            print(f'Creating intermodel {i+1}')
            interModel = HeModel()
            interController = HeController(interModel)
            interViewer = HeView(interModel)

            for patch in models[i].patches:
                for segment in patch.segments:
                    pt1 = Point(segment.pt1.x, segment.pt1.y)
                    pt2 = Point(segment.pt2.x, segment.pt2.y)
                    line = Line(pt1, pt2)

                    nSegmentsBefore = len(interViewer.getSegments())
                    interController.insertSegment(line, 0.1)
                    nSegmentsAfter = len(interViewer.getSegments())

                    if nSegmentsBefore != nSegmentsAfter:
                        interModel.segments[-1].setParentId(segment.parentId)

            for patch in models[i+1].patches:
                for segment in patch.segments:
                    pt1 = Point(segment.pt1.x, segment.pt1.y)
                    pt2 = Point(segment.pt2.x, segment.pt2.y)
                    line = Line(pt1, pt2)

                    nSegmentsBefore = len(interViewer.getSegments())
                    interController.insertSegment(line, 0.1)
                    nSegmentsAfter = len(interViewer.getSegments())

                    if nSegmentsBefore != nSegmentsAfter:
                        interModel.segments[-1].setParentId(segment.parentId)
            
            interModels.append(interModel)
            interControllers.append(interController)
            interViewers.append(interViewer)

        tf = perf_counter()
        
        print(f'Inter models created in {tf - ti:.5f} seconds.')

        ti = perf_counter()

        for i, model in enumerate(interModels):
            for patch in model.getPatches():
                patchIds = sorted(set([segment.parentId for segment in patch.segments]))
                bottomPatchesIds = [patchId for patchId in patchIds if patchId[0] == i+1]
                topPatchesIds = [patchId for patchId in patchIds if patchId[0] == i+2]

                if len(patchIds) > 1:

                    for botPatchId in bottomPatchesIds:
                        for topPatchId in topPatchesIds:
                            m, p = botPatchId
                            bottomPatch = models[m-1].patches[p-1]

                            m, p = topPatchId
                            topPatch = models[m-1].patches[p-1]

                            if topPatch not in bottomPatch.topConnections:
                                bottomPatch.addTopConnection(topPatch)

                            if bottomPatch not in topPatch.bottomConnections:
                                topPatch.addBottomConnection(bottomPatch)

                if len(patch.holes) > 0:
                    for hole in patch.holes:
                        holeId = hole[0].parentId

                        if holeId[0] == i+1:
                            m, p = holeId
                            bottomPatch = models[m-1].patches[p-1]

                            m, p = topPatchesIds[0]
                            topPatch = models[m-1].patches[p-1]
                        
                        if holeId[0] == i+2:
                            m, p = bottomPatchesIds[0]
                            bottomPatch = models[m-1].patches[p-1]

                            m, p = holeId
                            topPatch = models[m-1].patches[p-1]

                        if topPatch not in bottomPatch.topConnections:
                            bottomPatch.addTopConnection(topPatch)

                        if bottomPatch not in topPatch.bottomConnections:
                            topPatch.addBottomConnection(bottomPatch)

        tf = perf_counter()
        
        print(f'Connections done in {tf - ti:.5f} seconds.')

        ti = perf_counter()

        n = 0
        for i, model in enumerate(models):
            for j, patch in enumerate(model.getPatches()):
                if patch.region == None:
                    n += 1
                    enumerateRegion(patch, n)

        tf = perf_counter()
        
        print(f'{n} regions enumerated in {tf - ti:.5f} seconds.')

        ti = perf_counter()

        volumes = [0 for i in range(n)]
        for model in models:
            for patch in model.getPatches():
                volumes[patch.region-1] += int(patch.Area())

        zlen = len(dataset)
        ylen = len(dataset[0])
        xlen = len(dataset[0][0])
        tomoVolume = xlen * ylen * zlen

        print(f'All regions combined represent {(sum(volumes) / tomoVolume) * 100:.1f}% of total volume.')

        tf = perf_counter()
        
        print(f'Volumes calculated in {tf - ti:.5f} seconds.')

        ti = perf_counter()

        plt.figure(constrained_layout=True)
        plt.title('Regions Volume Distribution', fontsize=20)
        plt.xlabel('Region Volume', fontsize=20)
        plt.ylabel('Occurrences', fontsize=20)
        plt.xticks(fontsize=20)
        plt.yticks(fontsize=20)
        plt.grid()
        plt.hist(volumes, 5)
        plt.show()

        tf = perf_counter()
        
        print(f'Histogram done in {tf - ti:.5f} seconds.')

    # method
    def loadImageData(self, _filepath, _updateWindow):
        self.m_image = QtGui.QImage(_filepath)
        # We perform these conversions in order to deal with just 8 bits images:
        # convert Mono format to Indexed8
        if self.m_image.depth() == 1:
            self.m_image = self.m_image.convertToFormat(QtGui.QImage.Format_Indexed8)
        # convert Grayscale16 format to Grayscale8
        if not self.m_image.format() == QtGui.QImage.Format_Grayscale8:
            self.m_image = self.m_image.convertToFormat(QtGui.QImage.Format_Grayscale8)
        self.m_data = convertQImageToNumpy(self.m_image)
        if _updateWindow:
            self.labelDimensions.setText("[h="+str(self.m_data.shape[0])+",w="+str(self.m_data.shape[1])+"]")
            self.plotImage()

    # method
    def removeTempImagens(self):
        for filepath in self.m_map:
            if "temp_" in filepath :
                if os.path.exists(filepath):
                    try:
                        os.remove(filepath)
                    except OSError as err:
                        print("Exception handled: {0}".format(err))
                else:
                    print("The file does not exist") 

# This function was adapted from (https://github.com/Entscheider/SeamEater/blob/master/gui/QtTool.py)
# Project: SeamEater; Author: Entscheider; File: QtTool.py; GNU General Public License v3.0 
# Original function name: qimage2numpy(qimg)
# We consider just 8 bits images and convert to single depth:
def convertQImageToNumpy(_qimg):
    h = _qimg.height()
    w = _qimg.width()
    ow = _qimg.bytesPerLine() * 8 // _qimg.depth()
    d = 0
    if _qimg.format() in (QtGui.QImage.Format_ARGB32_Premultiplied,
                          QtGui.QImage.Format_ARGB32,
                          QtGui.QImage.Format_RGB32):
        d = 4 # formats: 6, 5, 4.
    elif _qimg.format() in (QtGui.QImage.Format_Indexed8,
                            QtGui.QImage.Format_Grayscale8):
        d = 1 # formats: 3, 24.
    else:
        raise ValueError(".ERROR: Unsupported QImage format!")
    buf = _qimg.bits().asstring(_qimg.byteCount())
    res = np.frombuffer(buf, 'uint8')
    res = res.reshape((h,ow,d)).copy()
    if w != ow:
        res = res[:,:w] 
    if d >= 3:
        res = res[:,:,0].copy()
    else:
        res = res[:,:,0] 
    return res 

def enumerateRegion(_patch, _region):
    _patch.setRegion(_region)
    
    if len(_patch.topConnections) > 0:
        for patch in _patch.topConnections:
            if patch.region is None:
                enumerateRegion(patch, _region)
    
    if len(_patch.bottomConnections) > 0:
        for patch in _patch.bottomConnections:
            if patch.region is None:
                enumerateRegion(patch, _region)
    
def main():
    # To ensure that every time you call QSettings not enter the data of your application, 
    # which will be the settings, you can set them globally for all applications   
    QtCore.QCoreApplication.setApplicationName(ORGANIZATION_NAME)
    QtCore.QCoreApplication.setOrganizationDomain(ORGANIZATION_DOMAIN)
    QtCore.QCoreApplication.setApplicationName(APPLICATION_NAME)
    # create pyqt5 app
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle('Fusion')
    # create the instance of our Window
    mw = TomoViewer()
    # showing all the widgets
    mw.show()
    # start the app
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
