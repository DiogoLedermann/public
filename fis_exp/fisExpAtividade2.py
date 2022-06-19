import xlsxwriter
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams

# 6) b)

def f(x):
    return a*x + b

# Contas

X = np.array([3.49, 4.26, 5.04, 6.06, 7.00, 7.57, 8.60, 9.25, 10.19, 10.96, 11.63, 12.50])
Y = np.array([1.20, 1.10, 1.00, 0.90, 0.80, 0.71, 0.60, 0.51, 0.41, 0.31, 0.21, 0.12])
sigmaX = 0.05
sigmaY = 0.04

n = len(X)
X2 = [x ** 2 for x in X]
XY = [x * y for x, y, in zip(X, Y)]

a = (n * sum(XY) - sum(X) * sum(Y)) / (n * sum(X2) - sum(X) ** 2)
b = (sum(Y) * sum(X2) - sum(X) * sum(XY)) / (n * sum(X2) - sum(X) ** 2)

realY = [f(x) for x in X]
deltaY = Y - realY
deltaY2 = deltaY ** 2

sums = [sum(X), sum(Y), sum(X2), sum(XY), sum(realY), sum(deltaY), sum(deltaY2)]

# table = np.zeros((n+1, 7))
# table[:-1, :] = np.array([X, Y, X2, XY, realY, deltaY, deltaY2]).transpose()
# table[-1:] = sums

aux = (sum(deltaY)**2) / (n-2)
sigmaA = np.sqrt((n*aux) / (n*sum(X2) - sum(X)**2))
sigmaB = np.sqrt((aux*sum(X2)) / (n*sum(X2) - sum(X)**2))

# Tabela no Excel

# workbook = xlsxwriter.Workbook('tabelaFeitaComPython.xlsx')
# worksheet = workbook.add_worksheet('Tabela')
#
# worksheet.set_column('F:H', 20)
#
# centralizado = workbook.add_format()
# decimais2 = workbook.add_format({'num_format': '#,##0.00'})
# decimais4 = workbook.add_format({'num_format': '#,####0.0000'})
# decimais16 = workbook.add_format({'num_format': '#,################0.0000000000000000'})
#
# centralizado.set_center_across()
# decimais2.set_center_across()
# decimais4.set_center_across()
# decimais16.set_center_across()
#
# # Column names
# r, c = 0, 1
# for name in ['xi', 'yi', 'xi²', 'xiyi', 'ax+b', 'Δy=yi-(ax+b)', '(Δy)²']:
#     worksheet.write(r, c, name, centralizado)
#     c += 1
#
# worksheet.write(13, 0, 'Σ', centralizado)
#
# # Table
# r, c = 1, 1
# for i, row in enumerate(table):
#     for j, element in enumerate(row):
#         if j < 2:
#             worksheet.write(r, c, element, decimais2)
#         elif  2 <= j < 4:
#             worksheet.write(r, c, element, decimais4)
#         else:
#             worksheet.write(r, c, element, decimais16)
#         c+=1
#     c = 1
#     r+=1
#
# # Extra variables
# r, c = 15, 1
# for variable, value in zip(['a', 'b', 'σa', 'σb'], [a, b, sigmaA, sigmaB]):
#     worksheet.write(r, c, variable, centralizado)
#     worksheet.write(r+1, c, value, centralizado)
#     c += 1
#
# workbook.close()

# Gráfico

plt.subplots(constrained_layout=True)
plt.title('Voltagem em função da corrente', fontsize=30)
rcParams.update({'font.size': 20})
plt.xlabel('I (mA)')
plt.ylabel('v (v)')
plt.xticks()
plt.yticks()
plt.grid()
for i, v in zip(X, Y):
    plt.plot(i, v, color='black', marker='o')
    plt.text(i+0.05, v+0.01, f'({i:.2f}, {v:.2f})')
    plt.plot([i - sigmaX, i + sigmaY], [v, v], color='red')
    plt.plot([i, i], [v - sigmaY, v + sigmaY], color='red')
xi, xf = min(X) - sigmaX, max(X) + sigmaY
plt.plot([xi, xf], [f(xi), f(xf)], label=f'{round(a, 5):.5f}x + {round(b, 5):.5f}')
plt.legend()
plt.show()
