import numpy as np

nR = 3
nC = 3

K = np.zeros((nR, nC))
F = np.zeros((nC, 1))
print(K)
print(F)

count = 0
for r in range(nR):
    for c in range(nC):
        K[r, c] = count + nR
        count = count + 1

for c in range(nC):
    F[c, 0] = c

print(K)
print(F)

D = np.linalg.solve(K, F)
print(D)