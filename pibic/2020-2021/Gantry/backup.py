import sys
import json
import numpy as np
import matplotlib.pyplot as plt
import scipy.optimize
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.Qt import *
np.set_printoptions(threshold=np.inf, linewidth=np.inf)

class ErrorDialog(QDialog):
    def __init__(self, erro, parent=None):
        super().__init__(parent=parent)

        self.setWindowTitle("Error")

        QBtn = QDialogButtonBox.Ok

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)

        self.layout = QVBoxLayout()
        message = QLabel(str(erro).capitalize())
        message.setAlignment(Qt.AlignHCenter)
        self.layout.addWidget(message)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)

class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.setWindowTitle("Gantry Reliability Analysis")
        self.setGeometry(0, 0, 800, 600)

        self.layout = QVBoxLayout()
        self.subLayout1 = QHBoxLayout()
        self.subLayout2 = QHBoxLayout()
        self.subLayout3 = QHBoxLayout()

        self.button1 = QPushButton('OPEN JSON FILE')
        self.button2 = QPushButton('RELIABILITY ANALYSIS')

        self.label1 = QLabel('JSON FILE PATH:')
        self.label2 = QLabel()
        self.label3 = QLabel('TRACTION BOUND:')
        self.label4 = QLabel('COMPRESSION BOUND:')
        self.label5 = QLabel('NUMBER OF TESTS:')
        self.label6 = QLabel('FAILURE RATE:')

        self.doubleSpinBox1 = QDoubleSpinBox()
        self.doubleSpinBox2 = QDoubleSpinBox()
        
        self.spinBox = QSpinBox()

        self.progressBar = QProgressBar()

        self.subLayout1.addWidget(self.label3)
        self.subLayout1.addWidget(self.doubleSpinBox1)

        self.subLayout2.addWidget(self.label4)
        self.subLayout2.addWidget(self.doubleSpinBox2)

        self.subLayout3.addWidget(self.label5)
        self.subLayout3.addWidget(self.spinBox)

        self.layout.addWidget(self.button1)
        self.layout.addWidget(self.label1)
        self.layout.addWidget(self.label2)
        self.layout.addLayout(self.subLayout1)
        self.layout.addLayout(self.subLayout2)
        self.layout.addLayout(self.subLayout3)
        self.layout.addWidget(self.button2)
        self.layout.addWidget(self.progressBar)
        self.layout.addWidget(self.label6)

        self.label1.setAlignment(Qt.AlignHCenter)
        self.label2.setAlignment(Qt.AlignHCenter)
        self.label3.setAlignment(Qt.AlignRight | Qt.AlignCenter)
        self.label4.setAlignment(Qt.AlignRight | Qt.AlignCenter)
        self.label5.setAlignment(Qt.AlignRight | Qt.AlignCenter)
        self.label6.setAlignment(Qt.AlignHCenter)
        self.progressBar.setAlignment(Qt.AlignHCenter)

        self.spinBox.setMaximum(1_000_000)
        self.doubleSpinBox1.setMaximum(np.inf)
        self.doubleSpinBox2.setMaximum(np.inf)
        self.spinBox.setValue(1)

        self.label2.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.MinimumExpanding)
        self.label2.setScaledContents(True)

        label6Font = QFont('Times', 12)
        label6Font.setBold(True)
        self.label6.setFont(label6Font)

        self.button1.setStatusTip('Open JSON file')
        self.button2.setStatusTip('Monte Carlo Reliability Analysis')

        self.button1.clicked.connect(self.button1_clicked)
        self.button2.clicked.connect(self.button2_clicked)

        widget = QWidget()
        widget.setLayout(self.layout)
        self.setCentralWidget(widget)
        self.setStatusBar(QStatusBar(self))

    def button1_clicked(self, s):
        try:
            self.path = QFileDialog.getOpenFileName()[0]
            self.label1.setText(f'JSON FILE PATH: {self.path}')

            with open(self.path) as file:
                self.data = json.load(file)
            
            nodes_coordinates = np.array(self.data['nodes coordinates'])
            restraints = np.array(self.data['restraints'])
            loads = np.array(self.data['loads'])
            connectivity = np.array(self.data['connectivity']) - 1

            plt.subplots(constrained_layout=True)
            plt.xticks(fontsize=8)
            plt.yticks(fontsize=8)
            plt.axis('equal')

            for i, element in enumerate(connectivity):
                color = 'blue'
                node_a, node_b = element
                a_x_coordinate, a_y_coordinate = nodes_coordinates[node_a]
                b_x_coordinate, b_y_coordinate = nodes_coordinates[node_b]
                x_mean = (a_x_coordinate + b_x_coordinate) / 2
                y_mean = (a_y_coordinate + b_y_coordinate) / 2
                plt.plot([a_x_coordinate, b_x_coordinate], [a_y_coordinate, b_y_coordinate], color=color, linewidth=3)
                plt.text(x_mean + 0.01, y_mean + 0.01, i + 1, color=color, fontsize=10)

            for i, node in enumerate(nodes_coordinates):
                x_coordinate, y_coordinate = node
                plt.plot(x_coordinate, y_coordinate, marker='o', color='black', markersize=6)
                plt.text(x_coordinate + 0.01, y_coordinate + 0.01, i + 1, fontsize=10)
                node_loads = np.array(loads[i])
                if any(node_loads != 0):
                    load_x_axis, load_y_axis, applied_moment = node_loads
                    scale = 0.4
                    width = 0.02
                    if load_x_axis < -0.5 or load_x_axis > 0.5:
                        plt.arrow(x_coordinate, y_coordinate, load_x_axis*scale, 0, width=width, length_includes_head=True,
                                color='black')
                    if load_y_axis < -0.5 or load_y_axis > 0.5:
                        plt.arrow(x_coordinate, y_coordinate, 0, load_y_axis*scale, width=width, length_includes_head=True,
                                color='black')
                node_restraints = np.array(restraints[i])
                if any(node_restraints != 0):
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
            
            plt.savefig('preview.png')
            self.label2.setPixmap(QPixmap('preview.png'))
                
            self.doubleSpinBox1.setValue(self.data['element properties'][1])
            self.doubleSpinBox2.setValue(abs(self.data['element properties'][0]))

        except Exception as erro:
            self.label1.setText('JSON FILE PATH:')
            self.label2.setText(' ')
            self.doubleSpinBox1.setValue(0)
            self.doubleSpinBox2.setValue(0)
            self.progressBar.setValue(0)
            self.label6.setText('FAILURE RATE:')
            dlg = ErrorDialog(erro)
            dlg.exec_()
    
    def button2_clicked(self, s):
        try:
            nodes_coordinates = np.array(self.data['nodes coordinates'])
            restraints = np.array(self.data['restraints'])
            loads = np.array(self.data['loads'])
            connectivity = np.array(self.data['connectivity']) - 1
            loads_std = self.data['loads std']
            element_properties = [-self.doubleSpinBox1.value(), self.doubleSpinBox2.value()]
            moment_capacity = self.data['moment capacity']
            properties_std = self.data['properties std']

            num_DOF = 3
            num_internal_forces = 3
            num_nodes = len(self.data['nodes coordinates'])
            num_elements = len(self.data['connectivity'])
            num_equations = num_nodes * num_DOF
            num_variables = 1 + num_elements * num_internal_forces

            objective_function = np.zeros(num_variables)
            objective_function[0] = -1

            A = np.zeros((num_equations, num_variables))
            for i, element in enumerate(connectivity):
                node_a, node_b = element
                x1, y1 = nodes_coordinates[node_a]
                x2, y2 = nodes_coordinates[node_b]
                delta_x = x2 - x1
                delta_y = y2 - y1
                L = np.sqrt(delta_x ** 2 + delta_y ** 2)
                cos_theta = delta_x / L
                sin_theta = delta_y / L
                values = np.array([[-cos_theta, -sin_theta/L, -sin_theta/L],
                                [-sin_theta, cos_theta/L, cos_theta/L],
                                [0, 1, 0],
                                [cos_theta, sin_theta/L, sin_theta/L],
                                [sin_theta, -cos_theta/L, -cos_theta/L],
                                [0, 0, 1]])
                rows = [node_a * 3, node_a * 3 + 1, node_a * 3 + 2, node_b * 3, node_b * 3 + 1, node_b * 3 + 2]
                A[rows, i * 3 + 1:i * 3 + 4] = - values
            restraints_reshaped = np.reshape(restraints, newshape=-1)
            indexes_to_be_deleted = [index for index, value in enumerate(restraints_reshaped) if value == 1]
            A = np.delete(A, indexes_to_be_deleted, axis=0)

            num_restraints = np.count_nonzero(self.data['restraints'])
            b = np.zeros(num_equations - num_restraints)

            num_tests = self.spinBox.value()
            self.progressBar.setMaximum(num_tests)
            num_failures = 0
            worst_lambda = 1
            properties = [element_properties] * num_elements
            for i in range(num_tests):
                updated_loads = np.random.normal(loads, scale=loads_std)
                loads_reshaped = np.reshape(updated_loads, newshape=-1)
                lambda_column = np.delete(loads_reshaped, indexes_to_be_deleted)
                A[:, 0] = lambda_column

                updated_properties = np.random.normal(properties, scale=properties_std)
                bounds = [[0, None]]
                for j in range(num_elements):
                    bounds.append(updated_properties[j])
                    bounds.append([-np.random.normal(moment_capacity, scale=properties_std),
                                    np.random.normal(moment_capacity, scale=properties_std)])
                    bounds.append([-np.random.normal(moment_capacity, scale=properties_std),
                                    np.random.normal(moment_capacity, scale=properties_std)])

                results = scipy.optimize.linprog(objective_function, A_eq=A, b_eq=b, bounds=bounds)
                solution = results.x
                solution_lambda = solution[0]
                if solution_lambda < 1:
                    num_failures += 1
                    if solution_lambda < worst_lambda:
                        worst_lambda = solution_lambda
                        worst_case = i + 1
                        worst_loads = updated_loads
                        worst_bounds = bounds
                        worst_solution = solution
                self.progressBar.setValue(i+1)

            failureRate = num_failures / num_tests

            plt.close()
            plt.subplots(constrained_layout=True)
            plt.xticks(fontsize=8)
            plt.yticks(fontsize=8)
            plt.axis('equal')
            if num_failures == 0:
                color = 'green'
                for i, element in enumerate(connectivity):
                    node_a, node_b = element
                    a_x_coordinate, a_y_coordinate = nodes_coordinates[node_a]
                    b_x_coordinate, b_y_coordinate = nodes_coordinates[node_b]
                    x_mean = (a_x_coordinate + b_x_coordinate) / 2
                    y_mean = (a_y_coordinate + b_y_coordinate) / 2
                    plt.plot([a_x_coordinate, b_x_coordinate], [a_y_coordinate, b_y_coordinate], color=color, linewidth=3)
                    plt.text(x_mean + 0.01, y_mean + 0.01, i + 1, color=color, fontsize=10)
            else:
                internal_forces = worst_solution[1:]
                elements_bounds = np.array(worst_bounds[1:])
                for i, element in enumerate(connectivity):
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
                    node_a, node_b = element
                    a_x_coordinate, a_y_coordinate = nodes_coordinates[node_a]
                    b_x_coordinate, b_y_coordinate = nodes_coordinates[node_b]
                    x_mean = (a_x_coordinate + b_x_coordinate) / 2
                    y_mean = (a_y_coordinate + b_y_coordinate) / 2
                    plt.plot([a_x_coordinate, b_x_coordinate], [a_y_coordinate, b_y_coordinate], color=color, linewidth=3)
                    plt.text(x_mean + 0.01, y_mean + 0.01, i + 1, color=color, fontsize=10)

            for i, node in enumerate(nodes_coordinates):
                x_coordinate, y_coordinate = node
                plt.plot(x_coordinate, y_coordinate, marker='o', color='black', markersize=6)
                plt.text(x_coordinate + 0.01, y_coordinate + 0.01, i + 1, fontsize=10)
                node_loads = np.array(loads[i])
                if any(node_loads != 0):
                    load_x_axis, load_y_axis, applied_moment = node_loads
                    scale = 0.4
                    width = 0.02
                    if load_x_axis < -0.5 or load_x_axis > 0.5:
                        plt.arrow(x_coordinate, y_coordinate, load_x_axis*scale, 0, width=width, length_includes_head=True,
                                color='black')
                    if load_y_axis < -0.5 or load_y_axis > 0.5:
                        plt.arrow(x_coordinate, y_coordinate, 0, load_y_axis*scale, width=width, length_includes_head=True,
                                color='black')
                node_restraints = np.array(restraints[i])
                if any(node_restraints != 0):
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

            plt.savefig('analysis.png', dpi=100)
            self.label2.setPixmap(QPixmap('analysis.png'))
            self.label6.setText(f'FAILURE RATE: {failureRate * 100:.2f}%')
        except Exception as erro:
            self.label1.setText('JSON FILE PATH:')
            self.label2.setText(' ')
            self.doubleSpinBox1.setValue(0)
            self.doubleSpinBox2.setValue(0)
            self.progressBar.setValue(0)
            self.label6.setText('FAILURE RATE:')
            dlg = ErrorDialog(erro)
            dlg.exec_()

app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec_()