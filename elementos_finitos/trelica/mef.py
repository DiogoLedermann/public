import numpy as np

def rigidezDoElemento(x1, y1, x2, y2, EA):
    dx = x2 - x1
    dy = y2 - y1
    L = np.sqrt(dx**2 + dy**2)
    cos = dx / L
    sin = dy / L
    R = np.array([[ cos, sin,    0,   0],
                  [-sin, cos,    0,   0],
                  [   0,   0,  cos, sin],
                  [   0,   0, -sin, cos]])
    kL = np.array([[EA/L, 0, -EA/L, 0], 
                  [    0, 0,     0, 0],
                  [-EA/L, 0,  EA/L, 0],
                  [    0, 0,     0, 0]])
    kG = R.T @ kL @ R
    return kG


def analise(coords, connect, forces, restrs, props):
    gdlNode = len(restrs[0])
    nodesPerElem = len(connect[0])
    gdlElem = gdlNode * nodesPerElem
    numElem = len(connect)
    numNodes = len(coords)
    K = np.zeros((numNodes*gdlNode, numNodes*gdlNode))
    F = np.zeros(numNodes*gdlNode)

    for e in range(numElem):
        n1, n2 = connect[e]
        x1, y1 = coords[n1-1]
        x2, y2 = coords[n2-1]
        EA = props[e]
        ke = rigidezDoElemento(x1, y1, x2, y2, EA)
        numGdl = len(connect[e]) * gdlNode
        gdlMap = [n1*2-2, n1*2-1, n2*2-2, n2*2-1]
        for r in range(gdlElem):
            for c in range(gdlElem):
                K[gdlMap[r], gdlMap[c]] += ke[r, c]

    for n in range(numNodes):
        rx, ry = restrs[n]
        if rx == 1:
            K[n*2, n*2] = 10**20
        if ry == 1:
            K[n*2+1, n*2+1] = 10**20
        fx, fy = forces[n]
        F[n*2] = fx
        F[n*2+1] = fy

    D = np.linalg.solve(K, F)
    
    S = []
    for e in range(numElem):
        n1, n2 = connect[e]
        x1, y1 = coords[n1-1]
        x2, y2 = coords[n2-1]
        dx = x2 - x1
        dy = y2 - y1
        L = np.sqrt(dx**2 + dy**2)
        cos = dx / L
        sin = dy / L
        EA = props[e]
        E = EA/(0.02*0.02)
        B = np.array([-1/L, 0, 1/L, 0])
        dG = [D[n1*2-2], D[n1*2-1], D[n2*2-2], D[n2*2-1]]
        R = np.array([[ cos, sin,    0,   0],
                      [-sin, cos,    0,   0],
                      [   0,   0,  cos, sin],
                      [   0,   0, -sin, cos]])
        dL = R @ dG
        s = E * B @ dL
        S.append(s)

    return D, S
