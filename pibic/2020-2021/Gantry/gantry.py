import json
import numpy as np

class Gantry():

    def __init__(self):
        self.nodesCoordinates = None
        self.restraints = None
        self.loads = None
        self.loadsStd = None
        self.connectivity = None
        self.elementProperties = None
        self.momentCapacity = None
        self.propertiesStd = None
    
    def fromJson(self, jsonFilePath):
        with open(jsonFilePath) as file:
            data = json.load(file)
        self.nodesCoordinates = data['nodes coordinates']
        self.restraints = data['restraints']
        self.loads = data['loads']
        self.loadsStd = data['loads std']
        self.connectivity = np.array(data['connectivity']) - 1
        self.elementProperties = data['element properties']
        self.momentCapacity = data['moment capacity']
        self.propertiesStd = data['properties std']
    
    def toJson(self):
        data = {
            'nodes coordinates': self.nodesCoordinates,
            'restraints': self.restraints,
            'loads': self.loads,
            'loads std': self.loadsStd,
            'connectivity': self.connectivity + 1,
            'element properties': self.elementProperties,
            'moment capacity': self.momentCapacity,
            'properties std': self.propertiesStd,
        }
        with open('data.txt', 'w') as outfile:
            json.dump(data, outfile)

    def setElementProperties(self, newElementProperties):
        self.elementProperties = newElementProperties
    
    def setMomentCapacity(self, newMomentCapacity):
        self.momentCapacity = newMomentCapacity
