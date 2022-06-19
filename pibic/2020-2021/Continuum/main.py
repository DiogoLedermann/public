import json
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize


def objectiveFunction(x):
    return -x[0]


def equalityConstraints(x):

    vector = np.zeros(numEquations)

    coefficientsMatrix = np.zeros((numEquations, numVariables))
    coefficientsMatrix[:, 0] = - loads.reshape(-1)

    for i, element in enumerate(connectivity):

        node1, node2, node3 = element

        rows = [node1 * 2, node1 * 2 + 1, node2 * 2, node2 * 2 + 1, node3 * 2, node3 * 2 + 1]
        columns = [i * 3 + 1, i * 3 + 2, i * 3 + 3]
        indexes = np.ix_(rows, columns)

        x1, y1 = nodesCoordinates[node1]
        x2, y2 = nodesCoordinates[node2]
        x3, y3 = nodesCoordinates[node3]

        values = (elementThicknes / 2) * np.array([[y2 - y3, 0, x3 - x2],
                                                   [0, x3 - x2, y2 - y3],
                                                   [y3 - y1, 0, x1 - x3],
                                                   [0, x1 - x3, y3 - y1],
                                                   [y1 - y2, 0, x2 - x1],
                                                   [0, x2 - x1, y1 - y2]])

        coefficientsMatrix[indexes] = values

    indexesToBeDeleted = np.nonzero(np.reshape(restraints, -1))
    coefficientsMatrix = np.delete(coefficientsMatrix, indexesToBeDeleted, axis=0)

    vector = coefficientsMatrix @ x

    return vector


def inequalityConstraints(x):

    vector = np.zeros(numElements)

    P = np.array([[1, -0.5, 0],
                  [-0.5, 1, 0],
                  [0, 0, 3]])

    for i in range(numElements):
        sigmaE = x[i * 3 + 1: i * 3 + 4]
        vector[i] = sigmaY - np.sqrt(sigmaE.T @ P @ sigmaE)

    return vector


with open('CNPq/2020-2021/continuumExample.json') as json_file:
    nodesCoordinates, restraints, loads, connectivity, elementThicknes, sigmaY = \
        [np.array(value) for value in json.load(json_file).values()]

connectivity -= 1

numNodes = len(nodesCoordinates)
numEquations = numNodes * 2
numElements = len(connectivity)
numVariables = 1 + numElements * 3

x0 = np.ones(numVariables)

eq_cons = {'type': 'eq',
           'fun': equalityConstraints}

ineq_cons = {'type': 'ineq',
             'fun': inequalityConstraints}

res = minimize(objectiveFunction, x0, method='SLSQP', constraints=[eq_cons, ineq_cons])
print(res)
