import numpy as np

def rigidezDoElemento(x1, x2, E, A):
    L = abs(x2-x1)
    k0 = E*A/L
    k = np.array([[k0, -k0], [-k0, k0]])
    return k


def analise(coords, connect, forces, restrs, props):
    numElem = len(connect)
    numNodes = len(coords)
    K = np.zeros((numNodes, numNodes))
    F = np.array(forces)
    for e in range(numElem):
        (n1, n2) = connect[e]
        x1 = coords[n1-1] 
        x2 = coords[n2-1]
        (E, A) = props[e]
        ke = rigidezDoElemento(x1, x2, E, A)
        numGdl = len(connect[e])
        gdlMap = [n1-1, n2-1]
        for r in range(numGdl):
            for c in range(numGdl):
                K[gdlMap[r], gdlMap[c]] += ke[r, c]
    for n in range(numNodes):
        if restrs[n] == 1:
            K[n, n] = 10**20
    w = np.linalg.eigvals(K)
    D = np.linalg.solve(K, F)
    for e in range(numElem):
        (n1, n2) = connect[e]
        x1 = coords[n1-1] 
        x2 = coords[n2-1]
        L = abs(x2-x1)
        (E, A) = props[e]
        B = np.array([-1/L, 1/L])
        d1 = D[n1-1]
        d2 = D[n2-1]
        d = [d1, d2]
        s = E * B @ d
        print(s)
    return D
