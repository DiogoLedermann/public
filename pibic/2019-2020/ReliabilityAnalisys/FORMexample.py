import numpy as np
import scipy.stats


def g(U):

    R, S = U

    return R - S


sigmaR = 2
miR = 10
sigmaS = 2
miS = 5

csiR = np.sqrt(np.log(1 + sigmaR**2 / miR**2))
lambdaR = np.log(miR) - csiR**2 / 2

gama = np.eye(2)

U = np.array([10, 5])

beta = 0
i = 0
while True:

    def stop_criteria(i, old, new):

        return True if i > 10 else abs(new - old) < 0.0001

    def print_iteration():

        print('-' * 30)
        print(f'Iteration: {i}')
        print(f'U: {[round(U[0], 3), round(U[1], 3)]}')
        print(f'sigma: {[round(sigmaNR, 3), round(sigmaNS, 3)]}')
        print(f'mi: {[round(miNR, 3), round(miNS, 3)]}')
        print(f'beta: {round(beta, 3)}')
        print(f'Unext: {[round(Unext[0], 3), round(Unext[1], 3)]}')
        print()

    i += 1

    R, S = U

    miNR = R * (1 - np.log(R) + lambdaR)
    sigmaNR = R*csiR

    miNS = miS
    sigmaNS = sigmaS

    sigma = np.array([[sigmaNR, 0], [0, sigmaNS]])
    m = np.array([miNR, miNS])

    J = np.matmul(gama, np.linalg.inv(sigma))

    gradGU = np.array([1, -1])

    tiJ = np.transpose(np.linalg.inv(J))

    gradGV = np.matmul(tiJ, gradGU)

    V = np.matmul(J, (U - m))

    Vnext = (1 / np.dot(gradGV, gradGV)) * ((np.transpose(gradGV) @ V) - g(U)) * gradGV

    old_beta = beta
    beta = np.sqrt(np.dot(Vnext, Vnext))

    Unext = U + np.transpose(np.linalg.inv(J)) @ (Vnext - V)

    print_iteration()

    if stop_criteria(i, old_beta, beta):
        break

    U = Unext

failure_probability = scipy.stats.norm.cdf(-beta)

print(f'Failure probabilty: {round(failure_probability, 3)}')
