import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.Qt import *

class CustomDialog(QDialog):
    def __init__(self, msg, parent=None):
        super().__init__(parent=parent)

        self.setWindowTitle("ERROR")

        QBtn = QDialogButtonBox.Ok

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)

        self.layout = QVBoxLayout()
        message = QLabel(msg)
        self.layout.addWidget(message)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)

class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.setWindowTitle("Calculadora RPN")

        layout = QVBoxLayout()

        self.visor = QLineEdit()

        botoes = QHBoxLayout()

        botao_backspace = QPushButton('←')
        botao_backspace.setStyleSheet('QPushButton {background-color: orange}')
        botao_backspace.clicked.connect(self.backspace)

        botao_clear = QPushButton('CE')
        botao_clear.setStyleSheet('QPushButton {background-color: orange}')
        botao_clear.clicked.connect(self.clear)

        botao_enter = QPushButton('Enter')
        botao_enter.setStyleSheet('QPushButton {background-color: lightgreen}')
        botao_enter.clicked.connect(self.enter)

        botoes.addWidget(botao_backspace)
        botoes.addWidget(botao_clear)
        botoes.addWidget(botao_enter)

        teclado = QGridLayout()

        botao1 = QPushButton('1')
        botao1.clicked.connect(self.botao1)
        botao2 = QPushButton('2')
        botao2.clicked.connect(self.botao2)
        botao3 = QPushButton('3')
        botao3.clicked.connect(self.botao3)
        botao4 = QPushButton('4')
        botao4.clicked.connect(self.botao4)
        botao5 = QPushButton('5')
        botao5.clicked.connect(self.botao5)
        botao6 = QPushButton('6')
        botao6.clicked.connect(self.botao6)
        botao7 = QPushButton('7')
        botao7.clicked.connect(self.botao7)
        botao8 = QPushButton('8')
        botao8.clicked.connect(self.botao8)
        botao9 = QPushButton('9')
        botao9.clicked.connect(self.botao9)
        botao0 = QPushButton('0')
        botao0.clicked.connect(self.botao0)
        botao_ponto = QPushButton('.')
        botao_ponto.clicked.connect(self.botao_ponto)

        teclado.addWidget(botao1, 0, 0)
        teclado.addWidget(botao2, 0, 1)
        teclado.addWidget(botao3, 0, 2)
        teclado.addWidget(botao4, 1, 0)
        teclado.addWidget(botao5, 1, 1)
        teclado.addWidget(botao6, 1, 2)
        teclado.addWidget(botao7, 2, 0)
        teclado.addWidget(botao8, 2, 1)
        teclado.addWidget(botao9, 2, 2)
        teclado.addWidget(botao0, 3, 1)
        teclado.addWidget(botao_ponto, 3, 2)

        operacoes = QHBoxLayout()
        
        botao_soma = QPushButton('+')
        botao_soma.setStyleSheet('QPushButton {background-color: lightblue}')
        botao_soma.clicked.connect(self.botao_soma)

        botao_subtracao = QPushButton('-')
        botao_subtracao.setStyleSheet('QPushButton {background-color: lightblue}')
        botao_subtracao.clicked.connect(self.botao_subtracao)

        botao_multiplicacao = QPushButton('x')
        botao_multiplicacao.setStyleSheet('QPushButton {background-color: lightblue}')
        botao_multiplicacao.clicked.connect(self.botao_multiplicacao)

        botao_divisao = QPushButton('÷')
        botao_divisao.setStyleSheet('QPushButton {background-color: lightblue}')
        botao_divisao.clicked.connect(self.botao_divisao)

        operacoes.addWidget(botao_soma)
        operacoes.addWidget(botao_subtracao)
        operacoes.addWidget(botao_multiplicacao)
        operacoes.addWidget(botao_divisao)
        
        self.pilha_label = QLabel('Pilha: ')
        self.pilha = []

        layout.addWidget(self.visor)
        layout.addLayout(botoes)
        layout.addLayout(teclado)
        layout.addLayout(operacoes)
        layout.addWidget(self.pilha_label)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)
    
    def backspace(self, s):
        self.visor.setText(self.visor.text()[:-1])
    
    def clear(self, s):
        self.pilha = []
        self.pilha_label.setText(f'Pilha: {self.pilha}')
        self.visor.setText('')
    
    def enter(self, s):
        try:
            self.pilha.append(float(self.visor.text()))
            self.pilha_label.setText(f'Pilha: {self.pilha}')
            self.visor.setText('')
        except Exception as erro:
            dlg = CustomDialog(str(erro))
            dlg.exec_()
    
    def botao1(self, s):
        self.visor.setText(self.visor.text() + '1')

    def botao2(self, s):
        self.visor.setText(self.visor.text() + '2')

    def botao3(self, s):
        self.visor.setText(self.visor.text() + '3')

    def botao4(self, s):
        self.visor.setText(self.visor.text() + '4')

    def botao5(self, s):
        self.visor.setText(self.visor.text() + '5')

    def botao6(self, s):
        self.visor.setText(self.visor.text() + '6')

    def botao7(self, s):
        self.visor.setText(self.visor.text() + '7')

    def botao8(self, s):
        self.visor.setText(self.visor.text() + '8')

    def botao9(self, s):
        self.visor.setText(self.visor.text() + '9')

    def botao0(self, s):
        self.visor.setText(self.visor.text() + '0')

    def botao_ponto(self, s):
        self.visor.setText(self.visor.text() + '.')

    def botao_soma(self, s):
        try:
            self.pilha[-2] = self.pilha[-2] + self.pilha[-1]
            del self.pilha[-1]
            self.pilha_label.setText(f'Pilha: {str(self.pilha)}')
        except Exception as erro:
            dlg = CustomDialog(str(erro))
            dlg.exec_()

    def botao_subtracao(self, s):
        try:
            self.pilha[-2] = self.pilha[-2] - self.pilha[-1]
            del self.pilha[-1]
            self.pilha_label.setText(f'Pilha: {str(self.pilha)}')
        except Exception as erro:
            dlg = CustomDialog(str(erro))
            dlg.exec_()

    def botao_multiplicacao(self, s):
        try:
            self.pilha[-2] = self.pilha[-2] * self.pilha[-1]
            del self.pilha[-1]
            self.pilha_label.setText(f'Pilha: {str(self.pilha)}')
        except Exception as erro:
            dlg = CustomDialog(str(erro))
            dlg.exec_()

    def botao_divisao(self, s):
        try:
            self.pilha[-2] = self.pilha[-2] / self.pilha[-1]
            del self.pilha[-1]
            self.pilha_label.setText(f'Pilha: {str(self.pilha)}')
        except Exception as erro:
            dlg = CustomDialog(str(erro))
            dlg.exec_()

app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec_()