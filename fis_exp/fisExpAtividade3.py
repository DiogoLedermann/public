import numpy as np
import matplotlib.pyplot as plt

distanciaData = [2, 4, 6, 8, 10]
forcaData = [2246.888, 561.722, 249.654, 140.430, 89.876]
sigmaX = 0.1

# plt.subplots(constrained_layout=True)
# plt.title('Força em funçao da carga', fontsize=30)
# plt.grid()
# plt.xlabel('L (cm)', fontsize=20)
# plt.ylabel('F (N)', fontsize=20)
# plt.xticks(fontsize=20)
# plt.yticks(fontsize=20)
# plt.scatter(distanciaData, forcaData, color='black')
# for x, y in zip(distanciaData, forcaData):
#     plt.text(x+0.05, y+0.01, f'({x:.2f}, {y:.2f})', fontsize=20)
#     plt.plot([x - sigmaX, x + sigmaX], [y, y], color='red')
# x = np.arange(2, 10.01, 0.01)
# k = 9 * 10**9
# q1,  q2 = 10 * 10**(-6), 10 * 10**(-6)
# y = []
# for L in x:
#     f = k*q1*q2 / (L/100)**2
#     y.append(f)
# plt.plot(x, y)
# plt.show()

k = np.array([8_987_500_000, 8_987_541_667, 8_987_550_000, 8_987_520_000, 8_987_600_000])
mk = np.mean(k)
sigmak = np.std(k)
print(f'{round(mk)} +/- {round(3*sigmak)}')
