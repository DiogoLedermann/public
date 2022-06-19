from FisExp.construtorDeGráficos import *

# Gráfico 1
X = [-73, 0, 127, 327, 527, 727, 927]
Y = [413, 401, 392, 383, 371, 357, 342]


if X[0] > X[-1]:
    X = [i for i in reversed(X)]
    Y = [i for i in reversed(Y)]

xticks = [i for i in np.arange(-100, 1000, 100)]
yticks = [i for i in np.arange(330, 430, 10)]

a, b, sigmaA, sigmaB = reta(X, Y)
# print(f'a = {a}, b = {b}, sigmaA = {sigmaA}, sigmaB={sigmaB}')

xvariable, xunit = 'Temperatura', '°C'
yvariable, yunit = 'Condutividade Térmica', 'W / m K'
variables = xvariable, xunit, yvariable, yunit

coefficients = plotPolyfit(X, Y, 6, 0.1, variables, xticks, yticks)
x = 100
print(f'f({x}) = {polynomial(x, coefficients)}')
ks = polynomial(x, coefficients)
