import matplotlib.pyplot as plt
import numpy as np

class DrawingTool():

    def __init__(self):
        plt.subplots(constrained_layout=True)
        plt.grid()
        plt.xticks(fontsize=8)
        plt.yticks(fontsize=8)
        plt.axis('equal')
    
    def plotElements(self, structure, brokenElements=None):
        for i, element in enumerate(structure.connectivity):
            node1, node2 = element
            node1x, node1y = structure.nodesCoordinates[node1]
            node2x, node2y = structure.nodesCoordinates[node2]
            xMean = (node1x + node2x) / 2
            yMean = (node1y + node2y) / 2
            if brokenElements is None:
                color = 'blue'
            elif brokenElements == []:
                color = 'green'
            else:
                if brokenElements[i] is True:
                    color = 'red'
                else:
                    color = 'blue'
            plt.plot([node1x, node2x], [node1y, node2y], color=color, linewidth=3)
            plt.text(xMean + 0.01, yMean + 0.01, i + 1, color=color, fontsize=10)

    def plotNodes(self, structure):
        for i, node in enumerate(structure.nodesCoordinates):
            xCoordinate, yCoordinate = node
            plt.plot(xCoordinate, yCoordinate, marker='o', color='black', markersize=6)
            plt.text(xCoordinate + 0.01, yCoordinate + 0.01, i + 1, fontsize=10)

    def plotRestraints(self, structure):
        for i, node in enumerate(structure.nodesCoordinates):
            x, y = node
            nodeRestraints = np.array(structure.restraints[i])
            if any(nodeRestraints == 1):
                xRestraint, yRestraint, momentRestraint = nodeRestraints
                if xRestraint == 1:
                    plt.plot([x, x-0.05, x+0.05, x], [y, y-0.1, y-0.1, y], color='black')
                if yRestraint == 1:
                    plt.plot([x, x-0.1, x-0.1, x], [y, y+0.05, y-0.05, y], color='black')

    def plotLoads(self, structure, tolerance=0.1, scale=0.5, width=0.02):
        for i, node in enumerate(structure.nodesCoordinates):
            x, y = node
            nodeLoads = np.array(structure.loads[i])
            if any(nodeLoads != 0):
                xLoad, yLoad, moment = nodeLoads
                if not (-tolerance < xLoad < tolerance):
                    plt.arrow(x, y, xLoad*scale, 0, width=width, length_includes_head=True, color='black')
                if not (-tolerance < yLoad < tolerance):
                    plt.arrow(x, y, 0, yLoad*scale, width=width, length_includes_head=True, color='black')

    def plotStructure(self, structure, brokenElements=None):
        if brokenElements is None:
            self.plotElements(structure)
        else:
            self.plotElements(structure, brokenElements)
        self.plotNodes(structure)
        self.plotRestraints(structure)
        self.plotLoads(structure)

    def getPath(self, fileName):
        plt.savefig(f'{fileName}.png')
        return f'{fileName}.png'
