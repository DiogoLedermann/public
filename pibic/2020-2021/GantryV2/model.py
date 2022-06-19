import json
import numpy as np
from os.path import dirname, realpath

class Node:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.xRestraint = False
        self.yRestraint = False
        self.momentRestraint = False
        self.xLoad = 0
        self.yLoad = 0
        self.moment = 0
    
    def __repr__(self):
        return f'({self.x}, {self.y})'
    
    def __eq__(self, other):
        return True if self.x == other.x and self.y == other.y else False

    def x(self):
        return self.x
    
    def y(self):
        return self.y
    
    def setXRestraint(self, value):
        self.xRestraint = value
    
    def setYRestraint(self, value):
        self.yRestraint = value
    
    def setMomentRestraint(self, value):
        self.momentRestraint = value
    
    def setXLoad(self, value):
        self.xLoad = value
    
    def setYLoad(self, value):
        self.yLoad = value
    
    def setMoment(self, value):
        self.moment = value

class Element:

    def __init__(self, n1, n2):
        self.n1 = n1
        self.n2 = n2
    
    def __repr__(self):
        return f'[{self.node1}, {self.node2}]'
    
    def __eq__(self, other):
        if (self.n1 == other.n1 and self.n2 == other.n2) or (self.n1 == other.n2 and self.n2 == other.n1):
            return True
        else:
            return False

    def notIn(self, elements):
        for element in elements:
            sameP1 = (self.n1.x == element.node1.x and self.n1.y == element.node1.y)
            sameP2 = (self.n2.x == element.node2.x and self.n2.y == element.node2.y)
            switchedP1 = (self.n1.x == element.node2.x and self.n1.y == element.node2.y)
            switchedP2 = (self.n2.x == element.node1.x and self.n2.y == element.node1.y)
            if (sameP1 and sameP2) or (switchedP1 and switchedP2):
                return False
        return True

class Model:

    def __init__(self):
        self.nodes = []
        self.elements = []
        self.solution = [np.inf]
        self.brokenElements = None
        self.compressionLimit = 0
        self.tractionLimit = 0
        self.momentLimit = 0
        self.solution = None

    def addNode(self, node):
        self.nodes.append(node)
    
    def addElement(self, element):
        self.elements.append(element)

    def delNode(self):
        try:
            del self.nodes[-1]
        except Exception:
            pass

    def delElement(self):
        try:
            del self.elements[-1]
        except Exception:
            pass
    
    def setCompressionLimit(self, value):
        self.compressionLimit = value

    def setTractionLimit(self, value):
        self.tractionLimit = value

    def setMomentLimit(self, value):
        self.momentLimit = value
    
    def fromJSON(self, fileName):
        self.__init__()
        with open(fileName) as file:
            data = json.load(file)
        
        for i, node in enumerate(data['nodes coordinates']):
            x, y = node

            xRestraint = data['restraints'][i][0]
            yRestraint = data['restraints'][i][1]
            momentRestraint = data['restraints'][i][2]

            xLoad = data['loads'][i][0]
            yLoad = data['loads'][i][1]
            moment = data['loads'][i][2]

            self.addNode(Node(x, y))
            self.nodes[i].setXRestraint(bool(xRestraint))
            self.nodes[i].setYRestraint(bool(yRestraint))
            self.nodes[i].setMomentRestraint(bool(momentRestraint))
            self.nodes[i].setXLoad(xLoad)
            self.nodes[i].setYLoad(yLoad)
            self.nodes[i].setMoment(moment)

        for i, element in enumerate(data['connectivity']):
            node1, node2 = element
            n1 = self.nodes[node1-1]
            n2 = self.nodes[node2-1]
            element = Element(n1, n2)
            self.addElement(element)
        
        self.compressionLimit = abs(data['element properties'][0])
        self.tractionLimit = data['element properties'][1]
        self.momentLimit = data['moment capacity']

    def toJSON(self, fileName):
        nodesCoordinates = [[node.x, node.y] for node in self.nodes]
        restraints = [[int(n.xRestraint), int(n.yRestraint), int(n.momentRestraint)] for n in self.nodes]
        loads = [[n.xLoad, n.yLoad, n.moment] for n in self.nodes]
        connectivity = [[self.nodes.index(element.n1)+1, self.nodes.index(element.n2)+1] for element in self.elements]
        elementProperties = [-self.compressionLimit, self.tractionLimit]

        data = {
            'nodes coordinates': nodesCoordinates,
            'restraints': restraints,
            'loads': loads,
            'connectivity': connectivity,
            'element properties': elementProperties,
            'moment capacity': self.momentLimit
        }

        dirName = dirname(realpath(__file__))
        with open(f'{dirName}\{fileName}.json', 'w') as outfile:
            json.dump(data, outfile, indent=1)
    
    def toIFC(self, fileName):
        nodesCoordinates = [[node.x, node.y] for node in self.nodes]
        connectivity = [[self.nodes.index(element.n1)+1, self.nodes.index(element.n2)+1] for element in self.elements]

        numElements = len(connectivity)
        t = 0.05

        newCoords = []
        for e in range(numElements):
            n1, n2 = connectivity[e]
            x1, y1 = nodesCoordinates[n1-1]
            x2, y2 = nodesCoordinates[n2-1]
            dx = x2 - x1
            dy = y2 - y1
            L = np.sqrt(dx**2 + dy**2)
            cos = dx / L
            sin = dy / L
            x = t * sin
            y = t * cos
            p1 = (-t*1000, (x1+x)*1000, (y1-y)*1000)
            p2 = (-t*1000, (x1-x)*1000, (y1+y)*1000)
            p3 = (t*1000, (x1-x)*1000, (y1+y)*1000)
            p4 = (t*1000, (x1+x)*1000, (y1-y)*1000)
            p5 = (-t*1000, (x2+x)*1000, (y2-y)*1000)
            p6 = (-t*1000, (x2-x)*1000, (y2+y)*1000)
            p7 = (t*1000, (x2-x)*1000, (y2+y)*1000)
            p8 = (t*1000, (x2+x)*1000, (y2-y)*1000)
            V = (p1, p2, p3, p4, p5, p6, p7, p8)
            newCoords.append(V)

        dir_name = dirname(realpath(__file__))
        with open(f'{dir_name}/{fileName}.ifc', 'w') as outfile:
            outfile.write(
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
                    + "'P-1','sample proxy',$,#1001,#1010,$,$);\n"
                "#1001= IFCLOCALPLACEMENT (#511,#1002);\n"
                "#1002= IFCAXIS2PLACEMENT3D (#1003,$,$);\n"
                "#1003= IFCCARTESIANPOINT ((1000.,0.,0.));\n")

            elements = []
            n = 1000
            for i in range(numElements):
                n += 20
                elements.append(n)
            indexes = elements
            elements = str(elements)

            i = 1
            for j in range(numElements):
                elements = elements[:i] + '#' + elements[i:]
                i = elements.find(',', i, len(elements))
                i += 2

            elements = elements.replace('[', '(')
            elements = elements.replace(']', ')')

            outfile.write \
                (f"#1010= IFCPRODUCTDEFINITIONSHAPE ($,$,{elements});\n")

            for i in range(numElements):
                outfile.write(
                    f"#{indexes[i]}= IFCSHAPEREPRESENTATION (#202,'Body',"
                        + f"'Tessellation',(#{indexes[i]+1}));\n"
                    f"#{indexes[i]+1}= IFCTRIANGULATEDFACESET "
                        + f"(#{indexes[i]+2},$,.T.,((1,6,5),(1,2,6),(6,2,7),"
                        + "(7,2,3),(7,8,6),(6,8,5),(5,8,1),(1,8,4),(4,2,1),"
                        + "(2,4,3),(4,8,7),(7,3,4)),$);\n"
                    f"#{indexes[i]+2}= IFCCARTESIANPOINTLIST3D "
                        + f"({newCoords[i]});\n")

            outfile.write(
                "#10000= IFCRELCONTAINEDINSPATIALSTRUCTURE "
                + "('2TnxZkTXT08eDuMuhUUFNy',$,'Physical model',$,(#1000), "
                + "#500);\n"
                "ENDSEC;\n"
                "END-ISO-10303-21;")

    def eraseBrokenElements(self):
        self.brokenElements = None
