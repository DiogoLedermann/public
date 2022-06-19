import numpy as np
from scipy.optimize import linprog


def limitAnalysis(gantry):
    degreesOfFreedom = 3
    numInternalForces = 3
    numNodes = len(gantry.nodesCoordinates)
    numElements = len(gantry.connectivity)
    numEquations = numNodes * degreesOfFreedom
    numVariables = 1 + numElements * numInternalForces

    objectiveFunction = np.zeros(numVariables)
    objectiveFunction[0] = -1

    A = np.zeros((numEquations, numVariables))
    lambdaColumn = np.reshape(gantry.loads, newshape=-1)
    A[:, 0] = lambdaColumn
    for i, element in enumerate(gantry.connectivity):
        node1, node2 = element
        x1, y1 = gantry.nodesCoordinates[node1]
        x2, y2 = gantry.nodesCoordinates[node2]
        deltaX = x2 - x1
        deltaY = y2 - y1
        L = np.sqrt(deltaX ** 2 + deltaY ** 2)
        cosTheta = deltaX / L
        sinTheta = deltaY / L
        values = np.array([[-cosTheta, -sinTheta/L, -sinTheta/L],
                           [-sinTheta,  cosTheta/L,  cosTheta/L],
                           [        0,           1,           0],
                           [ cosTheta,  sinTheta/L,  sinTheta/L],
                           [ sinTheta, -cosTheta/L, -cosTheta/L],
                           [        0,           0,           1]])
        rows = [node1 * 3, node1 * 3 + 1, node1 * 3 + 2, node2 * 3, node2 * 3 + 1, node2 * 3 + 2]
        A[rows, i * 3 + 1:i * 3 + 4] = - values
    restraintsReshaped = np.reshape(gantry.restraints, newshape=-1)
    indexesToBeDeleted = [index for index, value in enumerate(restraintsReshaped) if value == 1]
    A = np.delete(A, indexesToBeDeleted, axis=0)

    b = np.zeros(len(A))

    normalBounds = gantry.elementProperties
    momentBounds = [-gantry.momentCapacity, gantry.momentCapacity]

    bounds = [[0, None]] + [normalBounds, momentBounds, momentBounds] * numElements

    results = linprog(objectiveFunction, A_eq=A, b_eq=b, bounds=bounds)
    solution = results.x
    solutionLambda = solution[0]

    brokenElements = []
    if solutionLambda < 1:
        internalForces = solution[1:]
        elementsBounds = np.array(bounds[1:])
        for i in range(numElements):
            condition1 = (elementsBounds[i*3][0] < round(internalForces[i*3], 5) < elementsBounds[i*3][1])
            condition2 = (elementsBounds[i*3+1][0] < round(internalForces[i*3+1], 5) < elementsBounds[i*3+1][1])
            condition3 = (elementsBounds[i*3+2][0] < round(internalForces[i*3+2], 5) < elementsBounds[i*3+2][1])
            if (condition1 and condition2 and condition3):
                brokenElements.append(False)
            else:
                brokenElements.append(True)

    return solution, brokenElements
