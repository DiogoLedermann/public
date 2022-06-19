from scipy.optimize import linprog
from numpy import cos, array, zeros, sin
from math import radians

gravity = 9.81

Wa = 2 * gravity
Wb = 1.5 * gravity
Wc = 4 * gravity

Nab = Wa * cos(radians(30))
Nbc = Nab + Wb * cos(radians(30))
Nc = Nbc + Wc * cos(radians(30))

f = array([0, 0, 0, 0, 1])

A = array([[1, 0, 0, 0, -Nab],
           [-1, 0, 0, 0, -Nab],
           [0, 1, 0, 0, -Nbc],
           [0, -1, 0, 0, -Nbc],
           [0, 0, 1, 0, -Nc],
           [0, 0, -1, 0, -Nc]])

b = zeros(6)

Aeq = array([[-1, 0, 0, 1, 0],
             [1, -1, 0, 0, 0],
             [0, 1, 1, 1, 0]])

beq = array([[Wa*sin(radians(30))],
             [Wb*sin(radians(30))],
             [Wc*sin(radians(30))]])

bnds = (None, None, None, None, (0, None))

x = linprog(f, A_ub=A, b_ub=b, A_eq=Aeq, b_eq=beq, bounds=bnds)

print(x)
print()
