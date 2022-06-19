import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.Qt import *

class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.setWindowTitle("Calculadora RPN")

        self.centralWidget = QWidget()

        self.lineEdit = QLineEdit()

        self.button1 = QPushButton('←')
        self.button2 = QPushButton('CE')
        self.button3 = QPushButton('Enter')
        self.button4 = QPushButton('1')
        self.button5 = QPushButton('2')
        self.button6 = QPushButton('3')
        self.button7 = QPushButton('4')
        self.button8 = QPushButton('5')
        self.button9 = QPushButton('6')
        self.button10 = QPushButton('7')
        self.button11 = QPushButton('8')
        self.button12 = QPushButton('9')
        self.button13 = QPushButton('0')
        self.button14 = QPushButton('.')
        self.button15 = QPushButton('+')
        self.button16 = QPushButton('-')
        self.button17 = QPushButton('x')
        self.button18 = QPushButton('÷')

        self.label = QLabel('Pilha: ')
        
        self.layout = QVBoxLayout()
        self.sublayout1 = QHBoxLayout()
        self.sublayout2 = QGridLayout()
        self.sublayout3 = QHBoxLayout()

        self.sublayout1.addWidget(self.button1)
        self.sublayout1.addWidget(self.button2)
        self.sublayout1.addWidget(self.button3)

        self.sublayout2.addWidget(self.button4, 0, 0)
        self.sublayout2.addWidget(self.button5, 0, 1)
        self.sublayout2.addWidget(self.button6, 0, 2)
        self.sublayout2.addWidget(self.button7, 1, 0)
        self.sublayout2.addWidget(self.button8, 1, 1)
        self.sublayout2.addWidget(self.button9, 1, 2)
        self.sublayout2.addWidget(self.button10, 2, 0)
        self.sublayout2.addWidget(self.button11, 2, 1)
        self.sublayout2.addWidget(self.button12, 2, 2)
        self.sublayout2.addWidget(self.button13, 3, 1)
        self.sublayout2.addWidget(self.button14, 3, 2)

        self.sublayout3.addWidget(self.button15)
        self.sublayout3.addWidget(self.button16)
        self.sublayout3.addWidget(self.button17)
        self.sublayout3.addWidget(self.button18)

        self.layout.addWidget(self.lineEdit)
        self.layout.addLayout(self.sublayout1)
        self.layout.addLayout(self.sublayout2)
        self.layout.addLayout(self.sublayout3)
        self.layout.addWidget(self.label)

        self.centralWidget.setLayout(self.layout)

        self.setCentralWidget(self.centralWidget)

        self.button1.setStyleSheet('QPushButton {background-color: orange}')
        self.button2.setStyleSheet('QPushButton {background-color: orange}')
        self.button3.setStyleSheet('QPushButton {background-color: lightgreen}')
        self.button15.setStyleSheet('QPushButton {background-color: lightblue}')
        self.button16.setStyleSheet('QPushButton {background-color: lightblue}')
        self.button17.setStyleSheet('QPushButton {background-color: lightblue}')
        self.button18.setStyleSheet('QPushButton {background-color: lightblue}')

        self.label.setAlignment(Qt.AlignBottom)

        self.button1.clicked.connect(self.button1_clicked)
        self.button2.clicked.connect(self.button2_clicked)
        self.button4.clicked.connect(self.button4_clicked)
        self.button3.clicked.connect(self.button3_clicked)
        self.button5.clicked.connect(self.button5_clicked)
        self.button6.clicked.connect(self.button6_clicked)
        self.button7.clicked.connect(self.button7_clicked)
        self.button8.clicked.connect(self.button8_clicked)
        self.button9.clicked.connect(self.button9_clicked)
        self.button10.clicked.connect(self.button10_clicked)
        self.button11.clicked.connect(self.button11_clicked)
        self.button12.clicked.connect(self.button12_clicked)
        self.button13.clicked.connect(self.button13_clicked)
        self.button14.clicked.connect(self.button14_clicked)
        self.button15.clicked.connect(self.button15_clicked)
        self.button16.clicked.connect(self.button16_clicked)
        self.button17.clicked.connect(self.button17_clicked)
        self.button18.clicked.connect(self.button18_clicked)

        self.button4.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.MinimumExpanding)
        self.button5.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.MinimumExpanding)
        self.button6.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.MinimumExpanding)
        self.button7.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.MinimumExpanding)
        self.button8.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.MinimumExpanding)
        self.button9.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.MinimumExpanding)
        self.button10.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.MinimumExpanding)
        self.button11.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.MinimumExpanding)
        self.button12.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.MinimumExpanding)
        self.button13.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.MinimumExpanding)
        self.button14.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.MinimumExpanding)

        self.stack = []
    
    def button1_clicked(self):
        self.lineEdit.setText(self.lineEdit.text()[:-1])
    
    def button2_clicked(self):
        self.stack = []
        self.label.setText(f'Pilha: {self.stack}')
        self.lineEdit.setText('')
    
    def button3_clicked(self):
        try:
            self.stack.append(float(self.lineEdit.text()))
            self.label.setText(f'Pilha: {self.stack}')
            self.lineEdit.setText('')
        except:
            pass
    
    def button4_clicked(self):
        self.lineEdit.setText(self.lineEdit.text() + '1')
    
    def button5_clicked(self):
        self.lineEdit.setText(self.lineEdit.text() + '2')
    
    def button6_clicked(self):
        self.lineEdit.setText(self.lineEdit.text() + '3')
    
    def button7_clicked(self):
        self.lineEdit.setText(self.lineEdit.text() + '4')
    
    def button8_clicked(self):
        self.lineEdit.setText(self.lineEdit.text() + '5')
    
    def button9_clicked(self):
        self.lineEdit.setText(self.lineEdit.text() + '6')
    
    def button10_clicked(self):
        self.lineEdit.setText(self.lineEdit.text() + '7')
    
    def button11_clicked(self):
        self.lineEdit.setText(self.lineEdit.text() + '8')
    
    def button12_clicked(self):
        self.lineEdit.setText(self.lineEdit.text() + '9')
    
    def button13_clicked(self):
        self.lineEdit.setText(self.lineEdit.text() + '0')
    
    def button14_clicked(self):
        self.lineEdit.setText(self.lineEdit.text() + '.')
    
    def button15_clicked(self):
        try:
            self.stack[-2] = self.stack[-2] + self.stack[-1]
            del self.stack[-1]
            self.label.setText(f'Pilha: {str(self.stack)}')
        except:
            pass
    
    def button16_clicked(self):
        try:
            self.stack[-2] = self.stack[-2] - self.stack[-1]
            del self.stack[-1]
            self.label.setText(f'Pilha: {str(self.stack)}')
        except:
            pass
    
    def button17_clicked(self):
        try:
            self.stack[-2] = self.stack[-2] * self.stack[-1]
            del self.stack[-1]
            self.label.setText(f'Pilha: {str(self.stack)}')
        except:
            pass
    
    def button18_clicked(self):
        try:
            self.stack[-2] = self.stack[-2] / self.stack[-1]
            del self.stack[-1]
            self.label.setText(f'Pilha: {str(self.stack)}')
        except:
            pass

