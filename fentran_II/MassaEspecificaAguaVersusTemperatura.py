from FisExp.construtorDeGráficos import *

# Gráfico 1
X = [0, 4, 10, 15, 20, 22, 25, 30, 40, 60, 80, 100]
Y = [999.87, 1000, 999.73, 999.13, 998.23, 997.8, 997.07, 995.61, 992.2, 983.2, 971.8, 958.4]

if X[0] > X[-1]:
    X = [i for i in reversed(X)]
    Y = [i for i in reversed(Y)]

xticks = [i for i in np.arange(-10, 115, 5)]
yticks = [i for i in np.arange(950, 1100, 5)]

a, b, sigmaA, sigmaB = reta(X, Y)
# print(f'a = {a}, b = {b}, sigmaA = {sigmaA}, sigmaB={sigmaB}')

xvariable, xunit = 'Temperatura', '°C'
yvariable, yunit = 'Massa específica', 'kg/m³'
variables = xvariable, xunit, yvariable, yunit

coefficients = plotPolyfit(X, Y, 7, 0.1, variables, xticks, yticks)
x = 27
print(f'f({x}) = {polynomial(x, coefficients)}')
ro = polynomial(x, coefficients)
