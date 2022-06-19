import json
import numpy as np
import scipy.optimize
import scipy.stats
import matplotlib.pyplot as plt


def main():

    def get_data(_file_name):

        def fix(matrix):

            matrix = np.array(matrix) - 1

            return matrix

        with open(_file_name) as json_file:
            data = json.load(json_file)

        data['connectivity'] = fix(data['connectivity'])

        return data

    def get_coefficients(_numVariables):

        coefficients = np.zeros(_numVariables)
        coefficients[0] = -1

        return coefficients

    def equilibrium_equations_A(_numEquations, _numVariable):

        def lambda_column(matrix, _loads):

            loads = np.array(_loads).reshape(-1)

            matrix[:, 0] = loads

            return matrix

        def get_columns(_matrix):

            def get_values(_element):

                node_a, node_b = element

                x1, y1 = nodes_coordinates[node_a]
                x2, y2 = nodes_coordinates[node_b]

                delta_x = x2 - x1
                delta_y = y2 - y1

                L = np.sqrt(delta_x ** 2 + delta_y ** 2)

                cos_theta = delta_x / L
                sin_theta = delta_y / L

                if structure == 'truss':
                    values = np.array([-cos_theta, -sin_theta, cos_theta, sin_theta])
                    rows = [node_a * 2, node_a * 2 + 1, node_b * 2, node_b * 2 + 1]

                if structure == 'gantry':
                    values = np.array([[-cos_theta, -sin_theta / L, -sin_theta / L],
                                       [-sin_theta, cos_theta / L, cos_theta / L],
                                       [0, 1, 0],
                                       [cos_theta, sin_theta / L, sin_theta / L],
                                       [sin_theta, -cos_theta / L, -cos_theta / L],
                                       [0, 0, 1]])
                    rows = [node_a * 3, node_a * 3 + 1, node_a * 3 + 2, node_b * 3, node_b * 3 + 1, node_b * 3 + 2]

                return values, rows

            for i, element in enumerate(connectivity):

                values, rows = get_values(element)

                if structure == 'truss':
                    _matrix[rows, i + 1] = - values

                if structure == 'gantry':
                    _matrix[rows, i * 3 + 1:i * 3 + 4] = - values

            return _matrix

        def remove_redundant_rows(_matrix):

            restraints_reshaped = np.reshape(restraints, newshape=-1)
            indexes_to_be_deleted = [index for index, value in enumerate(restraints_reshaped) if value == 1]
            _matrix = np.delete(_matrix, indexes_to_be_deleted, axis=0)

            return _matrix

        connectivity = data['connectivity']
        nodes_coordinates = data['nodes coordinates']
        restraints = data['restraints']
        loads = data['loads']

        matrix = np.zeros((_numEquations, _numVariable))
        matrix = lambda_column(matrix, loads)
        matrix = get_columns(matrix)
        matrix = remove_redundant_rows(matrix)

        return matrix

    def equilibrium_equations_B(_numEquations):

        numRestraints = np.count_nonzero(data['restraints'])
        matrix = np.zeros(_numEquations - numRestraints)

        return matrix

    def form():

        def stop_criteria(i, new, old):

            return True if i == 5 else abs(new - old) < 0.0001

        def get_lambda(U):

            def get_bounds():

                return [(0, None)] + [(-miR, miR)] * numElements

            miR, miS = U

            A[:, 0] *= miS
            bounds = get_bounds()

            results = scipy.optimize.linprog(objective_function, A_eq=A, b_eq=b, bounds=bounds)
            solution = results.x
            solution_lambda = solution[0]

            return solution_lambda

        def get_gradGU(U):

            R, S = U

            deltaR = 0.001
            deltaS = 0.001

            U1 = R + deltaR, S
            U2 = R, S + deltaS

            lambda1 = get_lambda(U1)
            lambda2 = get_lambda(U2)

            f0 = 1 - lamb
            f1 = 1 - lambda1
            f2 = 1 - lambda2

            return [(f1 - f0) / deltaR, (f2 - f0) / deltaS]

        def g(solution_lambda):

            return 1 - solution_lambda

        def print_iteration():

            print('-' * 30)
            print(f'Iteration: {i}')
            print(f'U: {[round(U[0], 3), round(U[1], 3)]}')
            print(f'sigma: {[round(sigmaR, 3), round(sigmaS, 3)]}')
            print(f'mi: {[round(miR, 3), round(miS, 3)]}')
            print(f'beta: {round(beta, 3)}')
            print(f'Unext: {[round(Unext[0], 3), round(Unext[1], 3)]}')
            print()

        objective_function = get_coefficients(numVariables)
        A = equilibrium_equations_A(numEquations, numVariables)
        b = equilibrium_equations_B(numEquations)

        miR = data['element properties'][1]
        sigmaR = data['properties std']
        miS = 1
        sigmaS = data['loads std']
        U = miR, miS

        sigma = np.array([[sigmaR, 0], [0, sigmaS]])
        gama = np.eye(2)

        i, beta = 0, 0
        while True:

            i += 1
            print('i: ', i)

            lamb = get_lambda(U)

            m = np.array([miR, miS])

            J = np.matmul(gama, np.linalg.inv(sigma))

            gradGU = get_gradGU(U)

            tiJ = np.transpose(np.linalg.inv(J))

            gradGV = np.matmul(tiJ, gradGU)

            V = np.matmul(J, (U - m))

            Vnext = (1 / np.dot(gradGV, gradGV)) * ((np.transpose(gradGV) @ V) - g(lamb)) * gradGV

            old_beta = beta
            beta = np.sqrt(np.dot(Vnext, Vnext))

            Unext = U + np.transpose(np.linalg.inv(J)) @ (Vnext - V)

            print_iteration()

            if stop_criteria(i, old_beta, beta):

                failure_probability = scipy.stats.norm.cdf(-beta)

                return failure_probability

            U = Unext

            miR, miS = U

    np.set_printoptions(threshold=3000, edgeitems=3000, linewidth=3000)

    file_name = 'trussExample.json'

    data = get_data(file_name)

    structure = data['structure']

    if structure == 'truss':
        numDOF = 2
        numInternalForces = 1

    numNodes = len(data['nodes coordinates'])
    numElements = len(data['connectivity'])

    numEquations = numNodes * numDOF
    numVariables = 1 + numElements * numInternalForces

    failure_probability = form()

    print(f'Failure probabilty: {round(failure_probability, 3)}')

main()
