from PyQt5.QtWidgets import *
from PyQt5.uic import *


def backspace():
    ui.visor.setText(ui.visor.text()[:-1])


def ce():
    global stack
    stack = []
    ui.stack_label.setText(f'Stack: {stack}')
    ui.visor.setText('')


def enter():
    stack.append(float(ui.visor.text()))
    ui.stack_label.setText(f'Stack: {stack}')
    ui.visor.setText('')


def b1():
    ui.visor.setText(ui.visor.text() + '1')


def b2():
    ui.visor.setText(ui.visor.text() + '2')


def b3():
    ui.visor.setText(ui.visor.text() + '3')
    

def b4():
    ui.visor.setText(ui.visor.text() + '4')
    

def b5():
    ui.visor.setText(ui.visor.text() + '5')
    

def b6():
    ui.visor.setText(ui.visor.text() + '6')
    

def b7():
    ui.visor.setText(ui.visor.text() + '7')
    

def b8():
    ui.visor.setText(ui.visor.text() + '8')
    

def b9():
    ui.visor.setText(ui.visor.text() + '9')
    

def b0():
    ui.visor.setText(ui.visor.text() + '0')
    

def point():
    ui.visor.setText(ui.visor.text() + '.')


def add():
    stack[-2] = stack[-2] + stack[-1]
    del stack[-1]
    ui.stack_label.setText(f'Stack: {stack}')


def subtract():
    stack[-2] = stack[-2] - stack[-1]
    del stack[-1]
    ui.stack_label.setText(f'Stack: {stack}')


def multiply():
    stack[-2] = stack[-2] * stack[-1]
    del stack[-1]
    ui.stack_label.setText(f'Stack: {stack}')


def divide():
    stack[-2] = stack[-2] / stack[-1]
    del stack[-1]
    ui.stack_label.setText(f'Stack: {stack}')


app = QApplication([])
ui = loadUi('Designer/calculadora.ui')

ui.backspace.clicked.connect(backspace)
ui.ce.clicked.connect(ce)
ui.enter.clicked.connect(enter)

ui.b1.clicked.connect(b1)
ui.b2.clicked.connect(b2)
ui.b3.clicked.connect(b3)
ui.b4.clicked.connect(b4)
ui.b5.clicked.connect(b5)
ui.b6.clicked.connect(b6)
ui.b7.clicked.connect(b7)
ui.b8.clicked.connect(b8)
ui.b9.clicked.connect(b9)
ui.b0.clicked.connect(b0)
ui.point.clicked.connect(point)

ui.add.clicked.connect(add)
ui.subtract.clicked.connect(subtract)
ui.multiply.clicked.connect(multiply)
ui.divide.clicked.connect(divide)

stack = []
ui.stack_label.setText(f'Stack: {stack}')

ui.show()
app.exec()
