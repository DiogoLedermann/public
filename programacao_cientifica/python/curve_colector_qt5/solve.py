import numpy as np

a = np.array([
    [4,  3,  0],
    [3,  4, -1],
    [0, -1,  4]
])

b = np.array([
    24,
    30, 
    -24
])

x = np.linalg.solve(a, b)

print(x)
