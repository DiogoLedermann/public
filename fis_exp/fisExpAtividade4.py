import numpy as np
import matplotlib.pyplot as plt

d = [0.5, 1, 1.5, 2]
v = [12.8, 6.3, 3, 1.6]

x = np.arange(0.25, 2, 0.01)
y = 2* 9*10**9 / x**3

plt.subplots(constrained_layout=True)
plt.grid()
plt.scatter(d, v)
plt.plot(x, y)
plt.show()
