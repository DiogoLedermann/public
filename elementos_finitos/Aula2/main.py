from PyQt5.QtWidgets import *


def soma():
    res.setText(str(float(t1.text()) + float(t2.text())))


app = QApplication([])
w = QWidget()
w.setGeometry(200, 200, 180, 150)

r1 = QLabel(w)
r1.setText('A = ')
r1.move(10, 10)
t1 = QLineEdit(w)
t1.move(30, 10)

r2 = QLabel(w)
r2.setText('B = ')
r2.move(10, 50)
t2 = QLineEdit(w)
t2.move(30, 50)

res = QLineEdit(w)
res.move(30, 90)

b = QPushButton(w)
b.setText('Somar!')
b.move(30, 120)
b.clicked.connect(soma)

w.show()
app.exec_()
