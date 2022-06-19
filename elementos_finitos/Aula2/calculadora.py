from PyQt5.QtWidgets import *
from PyQt5.QtGui import *


def backspace_func():
    visor.setText(visor.text()[:-1])


def ce_func():
    global stack
    stack = []
    stack_label.setText(f'Stack: {stack}')
    visor.setText('')


def enter_func():
    stack.append(float(visor.text()))
    stack_label.setText(f'Stack: {stack}')
    visor.setText('')


def b1_func():
    visor.setText(visor.text() + '1')


def b2_func():
    visor.setText(visor.text() + '2')


def b3_func():
    visor.setText(visor.text() + '3')


def b4_func():
    visor.setText(visor.text() + '4')


def b5_func():
    visor.setText(visor.text() + '5')


def b6_func():
    visor.setText(visor.text() + '6')


def b7_func():
    visor.setText(visor.text() + '7')


def b8_func():
    visor.setText(visor.text() + '8')


def b9_func():
    visor.setText(visor.text() + '9')


def b0_func():
    visor.setText(visor.text() + '0')


def point_func():
    visor.setText(visor.text() + '.')


def somar():
    stack[-2] = stack[-2] + stack[-1]
    del stack[-1]
    stack_label.setText(f'Stack: {str(stack):1000}')


def subtrair():
    stack[-2] = stack[-2] - stack[-1]
    del stack[-1]
    stack_label.setText(f'Stack: {str(stack):1000}')


def multiplicar():
    stack[-2] = stack[-2] * stack[-1]
    del stack[-1]
    stack_label.setText(f'Stack: {str(stack):1000}')


def dividir():
    stack[-2] = stack[-2] / stack[-1]
    del stack[-1]
    stack_label.setText(f'Stack: {str(stack):1000}')


app = QApplication([])
widget = QWidget()
widget.setWindowTitle('Calculadora RPN')
widget.setGeometry(100, 100, 415, 220)

visor = QLineEdit(widget)
visor.move(10, 10)
visor.resize(235, 20)

backspace = QPushButton(widget)
backspace.setText('←')
backspace.move(10, 40)
backspace.setStyleSheet('QPushButton {background-color: orange}')
backspace.clicked.connect(backspace_func)

ce = QPushButton(widget)
ce.setText('CE')
ce.move(90, 40)
ce.setStyleSheet('QPushButton {background-color: orange}')
ce.clicked.connect(ce_func)

enter = QPushButton(widget)
enter.setText('Enter')
enter.move(170, 40)
enter.setStyleSheet('QPushButton {background-color: lightgreen}')
enter.clicked.connect(enter_func)

b1 = QPushButton(widget)
b1.setText('1')
b1.move(10, 70)
b1.clicked.connect(b1_func)

b2 = QPushButton(widget)
b2.setText('2')
b2.move(90, 70)
b2.clicked.connect(b2_func)

b3 = QPushButton(widget)
b3.setText('3')
b3.move(170, 70)
b3.clicked.connect(b3_func)

b4 = QPushButton(widget)
b4.setText('4')
b4.move(10, 100)
b4.clicked.connect(b4_func)

b5 = QPushButton(widget)
b5.setText('5')
b5.move(90, 100)
b5.clicked.connect(b5_func)

b6 = QPushButton(widget)
b6.setText('6')
b6.move(170, 100)
b6.clicked.connect(b6_func)

b7 = QPushButton(widget)
b7.setText('7')
b7.move(10, 130)
b7.clicked.connect(b7_func)

b8 = QPushButton(widget)
b8.setText('8')
b8.move(90, 130)
b8.clicked.connect(b8_func)

b9 = QPushButton(widget)
b9.setText('9')
b9.move(170, 130)
b9.clicked.connect(b9_func)

b0 = QPushButton(widget)
b0.setText('0')
b0.move(90, 160)
b0.clicked.connect(b0_func)

point = QPushButton(widget)
point.setText('.')
point.move(170, 160)
point.clicked.connect(point_func)

soma = QPushButton(widget)
soma.setText('+')
soma.move(250, 70)
soma.setStyleSheet('QPushButton {background-color: lightblue}')
soma.clicked.connect(somar)

subtrai = QPushButton(widget)
subtrai.setText('-')
subtrai.move(330, 70)
subtrai.setStyleSheet('QPushButton {background-color: lightblue}')
subtrai.clicked.connect(subtrair)

multiplica = QPushButton(widget)
multiplica.setText('x')
multiplica.move(250, 100)
multiplica.setStyleSheet('QPushButton {background-color: lightblue}')
multiplica.clicked.connect(multiplicar)

divide = QPushButton(widget)
divide.setText('÷')
divide.move(330, 100)
divide.setStyleSheet('QPushButton {background-color: lightblue}')
divide.clicked.connect(dividir)

stack = []
stack_label = QLabel(widget)
stack_label.setText(f'Stack: {str(stack):1000}')
stack_label.setFont(QFont('Arial', 14))
stack_label.move(10, 190)

widget.show()
app.exec_()
