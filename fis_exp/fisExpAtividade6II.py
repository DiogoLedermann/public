from FisExp.toolbox import *


# Gráfico 1
X = [8.00, 7.74, 7.50, 7.27, 7.06, 6.86]
Y = [40.00, 38.71, 37.50, 36.36, 35.29, 34.29]
variables = ('Corrente', 'A'), ('Tensão', 'V')
ticks = [i for i in np.arange(5, 12, 0.2)], [i for i in np.arange(20, 60, 2)]

graph((X, Y), variables, ticks, title='Tensão Vesus Corrente (R1)')


# Gráfico 2
X = [6.00, 5.85, 5.71, 5.58, 5.45, 5.33]
Y = [60.00, 58.54, 57.14, 55.81, 54.55, 53.33]
variables = ('Corrente', 'A'), ('Tensão', 'V')
ticks = [i for i in np.arange(4, 8, 0.1)], [i for i in np.arange(50, 65, 1)]

graph((X, Y), variables, ticks, title='Tensão Vesus Corrente (R2)')


# Gráfico 3
X = [4.80, 4.71, 4.62, 4.53, 4.44, 4.36]
Y = [72.00, 70.59, 69.23, 67.92, 66.67, 65.45]
variables = ('Corrente', 'A'), ('Tensão', 'V')
ticks = [i for i in np.arange(3, 6, 0.1)], [i for i in np.arange(60, 80, 1)]

graph((X, Y), variables, ticks, title='Tensão Vesus Corrente (Req em série)')


# Gráfico 4
X = [9.00, 8.67, 8.37, 8.09, 7.83, 7.58]
Y = [30.00, 28.92, 27.91, 26.97, 26.09, 25.26]
variables = ('Corrente', 'A'), ('Tensão', 'V')
ticks = [i for i in np.arange(6, 11, 0.2)], [i for i in np.arange(20, 40, 1)]

graph((X, Y), variables, ticks, title='Tensão Vesus Corrente (Req em paralelo)')
