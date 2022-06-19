from PyQt5.QtWidgets import (QMainWindow, QLineEdit, QPushButton, QVBoxLayout,
    QGridLayout, QWidget)

class View(QMainWindow):
    
    def __init__(self, *args, **kwargs):
        super(View, self).__init__(*args, **kwargs)

        self.setWindowTitle("Calculadora")
        self.create_widgets()
        self.set_layout()

    def create_widgets(self):
        self.line_edit = QLineEdit()
        
        self.button_open = QPushButton('(')
        self.button_close = QPushButton(')')
        self.button_delete = QPushButton('del')
        self.button_add = QPushButton('+')

        self.button_7 = QPushButton("7")
        self.button_8 = QPushButton("8")
        self.button_9 = QPushButton("9")
        self.button_subtract = QPushButton('-')

        self.button_4 = QPushButton("4")
        self.button_5 = QPushButton("5")
        self.button_6 = QPushButton("6")
        self.button_multiply = QPushButton('*')

        self.button_1 = QPushButton('1')
        self.button_2 = QPushButton("2")
        self.button_3 = QPushButton("3")
        self.button_divide = QPushButton('/')

        self.button_opposite = QPushButton("+/-")
        self.button_0 = QPushButton("0")
        self.button_point = QPushButton(".")
        self.button_equals = QPushButton('=')

    def set_layout(self):
        sublayout = QGridLayout()

        sublayout.addWidget(self.button_open, 0, 0)
        sublayout.addWidget(self.button_close, 0, 1)
        sublayout.addWidget(self.button_delete, 0, 2)
        sublayout.addWidget(self.button_add, 0, 3)
        
        sublayout.addWidget(self.button_7, 1, 0)
        sublayout.addWidget(self.button_8, 1, 1)
        sublayout.addWidget(self.button_9, 1, 2)
        sublayout.addWidget(self.button_subtract, 1, 3)

        sublayout.addWidget(self.button_4, 2, 0)
        sublayout.addWidget(self.button_5, 2, 1)
        sublayout.addWidget(self.button_6, 2, 2)
        sublayout.addWidget(self.button_multiply, 2, 3)

        sublayout.addWidget(self.button_1, 3, 0)
        sublayout.addWidget(self.button_2, 3, 1)
        sublayout.addWidget(self.button_3, 3, 2)
        sublayout.addWidget(self.button_divide, 3, 3)

        sublayout.addWidget(self.button_opposite, 4, 0)
        sublayout.addWidget(self.button_0, 4, 1)
        sublayout.addWidget(self.button_point, 4, 2)
        sublayout.addWidget(self.button_equals, 4, 3)
        
        layout = QVBoxLayout()
        layout.addWidget(self.line_edit)
        layout.addLayout(sublayout)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)
