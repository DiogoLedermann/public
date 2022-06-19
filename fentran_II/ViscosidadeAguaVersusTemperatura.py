from FisExp.construtorDeGráficos import *

# Gráfico 1
X = [0, 5, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
Y = [1.787, 1.519, 1.307, 1.002, 0.798, 0.653, 0.547, 0.467, 0.404, 0.355, 0.315, 0.282]

if X[0] > X[-1]:
    X = [i for i in reversed(X)]
    Y = [i for i in reversed(Y)]

xticks = [i for i in np.arange(-10, 115, 5)]
yticks = [i for i in np.arange(0, 2.2, 0.2)]

a, b, sigmaA, sigmaB = reta(X, Y)
# print(f'a = {a}, b = {b}, sigmaA = {sigmaA}, sigmaB={sigmaB}')

xvariable, xunit = 'Temperatura', '°C'
yvariable, yunit = 'Viscosidade Dinâmica', 'N s/m²'
variables = xvariable, xunit, yvariable, yunit

plotPolyfit(X, Y, 10, 0.1, variables, xticks, yticks)
