import json
import numpy as np
import scipy.optimize
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
                    values = np.array([[-cos_theta, -sin_theta/L, -sin_theta/L],
                                       [-sin_theta, cos_theta/L, cos_theta/L],
                                       [0, 1, 0],
                                       [cos_theta, sin_theta/L, sin_theta/L],
                                       [sin_theta, -cos_theta/L, -cos_theta/L],
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

        matrix = np.zeros((_numEquations, _numVariable))
        matrix = get_columns(matrix)
        matrix = remove_redundant_rows(matrix)

        return matrix

    def equilibrium_equations_B(_numEquations):

        numRestraints = np.count_nonzero(data['restraints'])
        matrix = np.zeros(_numEquations - numRestraints)

        return matrix

    def monte_carlo(_numTests):

        def lambda_column(_updated_loads):

            loads_reshaped = np.reshape(_updated_loads, newshape=-1)
            restraints_reshaped = np.reshape(restraints, newshape=-1)
            indexes_to_be_deleted = [index for index, value in enumerate(restraints_reshaped) if value == 1]
            column = np.delete(loads_reshaped, indexes_to_be_deleted)

            return column

        def get_bounds(_updated_properties, _moment_capacity):

            bounds = [[0, None]]
            
            if structure == 'truss':

                for pair_of_bounds in _updated_properties:
                    bounds.append(pair_of_bounds)
            
            if structure == 'gantry':

                for i in range(numElements):

                    bounds.append(_updated_properties[i])

                    bounds.append([-np.random.normal(_moment_capacity, scale=properties_std),
                                   np.random.normal(_moment_capacity, scale=properties_std)])

                    bounds.append([-np.random.normal(_moment_capacity, scale=properties_std),
                                   np.random.normal(_moment_capacity, scale=properties_std)])

            return bounds

        def print_iteration():

            def print_internal_forces(precision=3):

                if structure == 'gantry':

                    indexes = []

                    for i in range(numElements):

                        j = i * 2
                        k = i * 2 + 1

                        indexes.append(i)
                        indexes.append(j)
                        indexes.append(k)

                letter = 'N'

                internal_forces = solution[1:]
                elements_bounds = bounds[1:]

                for i, tuple in enumerate(zip(internal_forces, elements_bounds)):

                    if structure == 'gantry':

                        if i % 3 != 0:
                            letter = 'M'

                        i = indexes[i]

                    value, pair_of_bounds = tuple

                    value = round(value, precision)

                    L_bound, U_bound = pair_of_bounds
                    L_bound, U_bound = round(L_bound, precision), round(U_bound, precision)

                    blue = '\033[34m'

                    if value == L_bound or value == U_bound:
                        print(f'{red}{letter}{i + 1} = {value}{white}')
                    else:
                        print(f'{blue}{letter}{i + 1}{white} = {value}')

                    letter = 'N'

            print(f'Test {i + 1}')

            white, red, green = '\033[30m', '\033[31m', '\033[32m'

            if solution_lambda > 1:
                print(f'{green}lambda{white} = {solution_lambda}')
            else:
                print(f'{red}lambda{white} = {solution_lambda}')
                print_internal_forces()

            print()

        loads = data['loads']
        properties = [data['element properties']] * numElements
        restraints = data['restraints']
        loads_std = data['loads std']
        properties_std = data['properties std']
        moment_capacity = data['moment capacity']

        numFailures = 0
        worst_lambda = 1
        worst_case = None

        for i in range(_numTests):

            updated_loads = np.random.normal(loads, scale=loads_std)
            updated_properties = np.random.normal(properties, scale=properties_std)

            A[:, 0] = lambda_column(updated_loads)
            bounds = get_bounds(updated_properties, moment_capacity)

            results = scipy.optimize.linprog(objective_function, A_eq=A, b_eq=b, bounds=bounds)
            solution = results.x
            solution_lambda = solution[0]

            if solution_lambda < 1:
                numFailures += 1

                if solution_lambda < worst_lambda:
                    worst_lambda = solution_lambda
                    worst_case = i, updated_loads, bounds, solution

            print_iteration()

        return numFailures, worst_case

    def show_truss(_worst_case):

        def plot_nodes():

            def plot_loads(scale=0.1, tolerance=2):

                if structure == 'truss':
                    load_x_axis, load_y_axis = node_loads

                if structure == 'gantry':
                    load_x_axis, load_y_axis, applied_moment = node_loads

                if load_x_axis < -tolerance or load_x_axis > tolerance:
                    plt.arrow(x_coordinate, y_coordinate, load_x_axis*scale, 0, width=0.1, length_includes_head=True,
                              color='black')

                if load_y_axis < -tolerance or load_y_axis > tolerance:
                    plt.arrow(x_coordinate, y_coordinate, 0, load_y_axis*scale, width=0.1, length_includes_head=True,
                              color='black')

            def plot_restraints():

                if structure == 'truss':
                    restraint_x_axis, restraint_y_axis = node_restraints

                if structure == 'gantry':
                    restraint_x_axis, restraint_y_axis, moment_restraint = node_restraints

                if restraint_x_axis != 0:
                    plt.plot([x_coordinate - 0.1, x_coordinate - 0.1], [y_coordinate - 0.05, y_coordinate + 0.05],
                             color='black')
                    plt.plot([x_coordinate - 0.1, x_coordinate], [y_coordinate - 0.05, y_coordinate], color='black')
                    plt.plot([x_coordinate - 0.1, x_coordinate], [y_coordinate + 0.05, y_coordinate], color='black')

                if restraint_y_axis != 0:
                    plt.plot([x_coordinate - 0.05, x_coordinate + 0.05], [y_coordinate - 0.1, y_coordinate - 0.1],
                             color='black')
                    plt.plot([x_coordinate - 0.05, x_coordinate], [y_coordinate - 0.1, y_coordinate], color='black')
                    plt.plot([x_coordinate, x_coordinate + 0.05], [y_coordinate, y_coordinate - 0.1], color='black')

            for i, node in enumerate(nodes_coordinates):

                x_coordinate, y_coordinate = node

                plt.plot(x_coordinate, y_coordinate, marker='o', color='black', markersize=10)
                plt.text(x_coordinate + 0.01, y_coordinate + 0.01, i + 1, fontsize=30)

                node_loads = np.array(loads[i])
                if any(node_loads != 0):
                    plot_loads(scale=0.04)

                node_restraints = np.array(restraints[i])
                if any(node_restraints != 0):
                    plot_restraints()

        def plot_elements():

            def set_element_color():

                if structure == 'truss':

                    Ni = internal_forces[i]
                    Ni = round(Ni, 3)

                    L_bound, U_bound = elements_bounds[i]
                    L_bound, U_bound = round(L_bound, 3), round(U_bound, 3)

                    if Ni == L_bound or Ni == U_bound:
                        color = 'red'
                    else:
                        color = 'blue'

                    return color

                if structure == 'gantry':

                    Ni, Mi1, Mi2 = internal_forces[i*3], internal_forces[i*3 + 1], internal_forces[i*3 + 2]
                    Ni, Mi1, Mi2 = round(Ni, 3), round(Mi1, 3), round(Mi2, 3)

                    Ni_L_bound, Ni_U_bound = elements_bounds[i*3]
                    Mi1_L_bound, Mi1_U_bound = elements_bounds[i*3 + 1]
                    Mi2_L_bound, Mi2_U_bound = elements_bounds[i*3 + 2]

                    Ni_L_bound, Ni_U_bound = round(Ni_L_bound, 3), round(Ni_U_bound, 3)
                    Mi1_L_bound, Mi1_U_bound = round(Mi1_L_bound, 3), round(Mi1_U_bound, 3)
                    Mi2_L_bound, Mi2_U_bound = round(Mi2_L_bound, 3), round(Mi2_U_bound, 3)

                    if (Ni == Ni_L_bound or Ni == Ni_U_bound) or \
                       (Mi1 == Mi1_L_bound or Mi1 == Mi1_U_bound) or \
                       (Mi2 == Mi2_L_bound or Mi2 == Mi2_U_bound):
                        color = 'red'
                    else:
                        color = 'blue'

                    return color

            internal_forces = solution[1:]
            elements_bounds = bounds[1:]

            for i, element in enumerate(connectivity):

                color = set_element_color()

                node_a, node_b = element

                a_x_coordinate, a_y_coordinate = nodes_coordinates[node_a]
                b_x_coordinate, b_y_coordinate = nodes_coordinates[node_b]

                x_mean = (a_x_coordinate + b_x_coordinate) / 2
                y_mean = (a_y_coordinate + b_y_coordinate) / 2

                plt.plot([a_x_coordinate, b_x_coordinate], [a_y_coordinate, b_y_coordinate], color=color, linewidth=3)
                plt.text(x_mean + 0.01, y_mean + 0.01, i + 1, color=color, fontsize=30)

        i, loads, bounds, solution = _worst_case

        nodes_coordinates = data['nodes coordinates']
        restraints = data['restraints']
        connectivity = data['connectivity']

        plt.subplots(constrained_layout=True)
        plt.title(f'Worst Case: Test {i+1}', fontsize=30)
        # plt.grid()
        plt.xticks(fontsize=20)
        plt.yticks(fontsize=20)
        plot_nodes()
        plot_elements()
        plt.show()

    file_name = 'trussExample4.json'

    data = get_data(file_name)

    structure = data['structure']

    if structure == 'truss':
        numDOF = 2
        numInternalForces = 1
    
    if structure == 'gantry':
        numDOF = 3
        numInternalForces = 3

    numNodes = len(data['nodes coordinates'])
    numElements = len(data['connectivity'])

    numEquations = numNodes * numDOF
    numVariables = 1 + numElements * numInternalForces

    objective_function = get_coefficients(numVariables)
    A = equilibrium_equations_A(numEquations, numVariables)
    b = equilibrium_equations_B(numEquations)

    numTests = 1

    numFailures, worst_case = monte_carlo(numTests)

    failure_rate = numFailures / numTests

    print(f'Tests: {numTests}')
    print(f'Failures: {numFailures}')
    print(f'Failure rate: {failure_rate * 100}%')

    if numFailures != 0:
        show_truss(worst_case)


main()
