import numpy as np
import matplotlib.pyplot as plt
from math import log


def f(x, a, b):
    return a * log(x) + b


X1 = np.array([1980, 1990, 2000, 2010, 2020])
Y1 = np.array([32618, 46542, 76556, 127461, 164504])

a, b = np.polyfit(log(X1), Y1, 1)
print(a, b)

X2 = [i for i in range(1980, 2051, 1)]
Y2 = [f(x) for x in X2]

plt.figure()
plt.plot(X1, Y1, marker='o')
plt.plot(X2, Y2)
plt.show()
