from FisExp.toolbox import *

X = [0.50, 1.00, 1.50, 2.00, 2.50, 3.00, 3.50, 4.00]
Y = [9.45, 18.9, 28.35, 37.79, 47.15, 56.69, 66.14, 73.6]

variables = ('Comprimento', 'mm'), ('∫ A B dl', 'mT mm')
ticks = 1, 1

a, b, sA = linearRegression(X, Y)
generalForm(a, sA)
graph((X, Y), variables, ticks, label=f'y = ({a})x + ({b})')
