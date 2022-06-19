from FisExp.toolbox import *

# Gráfico 1
X = [2.01, 4.01, 6.01, 8.01, 10.01, 12.01, 14.01]
Y = [0.134, 0.267, 0.401, 0.534, 0.667, 0.801, 0.934]
variables = ('Comprimento', 'cm'), ('Resistência', 'Ω')
gridscale = 2, 0.1

a, b, sA = linearRegression(X, Y)
generalForm(a, sA, 7.5, 'ρ', 'Ωcm', 6)
graph((X, Y), variables, gridscale, label=f'y = ({a})x + ({b})')

# Gráfico 2
X = [2.02, 4.01, 6.00, 7.99, 9.98, 12.02, 14.01]
Y = [2.48, 1.25, 0.833, 0.626, 0.501, 0.416, 0.357]
xticks, yticks = getTicks((X, Y), (2, 0.5))

fs = 30
plt.subplots(constrained_layout=True)
plt.title(f'Resistência Versus Área', fontsize=fs+10)
plt.xlabel('Área (cm²)', fontsize=fs)
plt.ylabel('Resistência (Ω)', fontsize=fs)
plt.xticks(xticks, fontsize=fs)
plt.yticks(yticks, fontsize=fs)
plt.grid()
plt.scatter(X, Y, color='black', s=80)
xvalues = [i for i in np.arange(1.5, 18, 0.1)]
yvalues = [5/x for x in xvalues]
plt.plot(xvalues, yvalues, label='y = 10 ρ / x')
plt.legend(loc='best', fontsize=fs-5)
plt.show()

# Gráfico 3
X = [0.50, 0.25, 0.17, 0.13, 0.10, 0.08, 0.07]
Y = [2.48, 1.25, 0.833, 0.626, 0.501, 0.416, 0.357]
variables = ('1 / Área', 'cm⁻²'), ('Resistência', 'Ω')
gridscale = 0.05, 0.5

a, b, sA = linearRegression(X, Y)
generalForm(a, sA, 0.1, 'ρ', 'Ωcm', 3)
graph((X, Y), variables, gridscale, label=f'y = ({a})x + ({b})')
