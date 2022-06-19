import numpy as np
import matplotlib.pyplot as plt

r = [200, 400, 600, 800, 1000]
i = [22.5, 11.3, 7.5, 5.6, 4.5]

plt.subplots(constrained_layout=True)
plt.title('Corrente em função da resistência', fontsize=30)
plt.xlabel('Resistência (Ω)', fontsize=20)
plt.ylabel('Corrente (mA)', fontsize=20)
plt.xticks(r, fontsize=20)
plt.yticks(i, fontsize=20)
plt.grid()
plt.scatter(r, i, color='black')
x = np.arange(200, 1000, 1)
r = [4.5] * 800
plt.plot(x, (r/x)*1000, label='4.5/R')
plt.legend()
plt.show()
