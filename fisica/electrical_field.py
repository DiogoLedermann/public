import numpy as np
import matplotlib.pyplot as plt


def F(x, y):
    fx, fy = 0, 0
    for charge in charges:
        q, position = charge
        xi, yi = position
        k = 9 * 10 ** 9
        dx = xi - x
        dy = yi - y
        d = np.sqrt(dx**2 + dy**2)
        E = (k*q)/(d**2)
        cos = dx / d
        sin = dy / d
        fx += E*cos
        fy += E*sin
    return fx, fy


charges = [[1, (-1, 0)], [-1, (1, 0)]]

plt.subplots(constrained_layout=True)
plt.grid()

for value, position in charges:
    
    if value > 0:
        color = 'red'
    elif value < 0 :
        color = 'blue'
    else:
        color = 'black'
        
    x, y = position
    plt.plot(x, y, marker='o', color=color)
    plt.text(x+0.01, y+0.005, value)

X, Y = np.meshgrid(np.arange(-2, 2, 0.1), np.arange(-1, 1, 0.1))
U, V = F(X, Y)

plt.streamplot(X, Y, U, V)

plt.show()
