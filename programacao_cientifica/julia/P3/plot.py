import json
import numpy as np
import matplotlib.pyplot as plt


def T(Tinf, A, B, lamb, x):
    return Tinf + A * np.e ** (lamb * x) + B * np.e ** (- lamb * x)

with open('input.json') as file:
    data = json.load(file)

h_ = data["h'"]
h = data["h"]
r = data["r"]
k = data["k"]
Tinf = data["Tinf"]
Ta = data["Ta"]
Tb = data["Tb"]
L = data["L"]
dx = data["dx"]

lamb = np.sqrt(h_)

t = [i for i in np.arange(0 + dx, L, dx)]
print(t)

aux1 = np.e ** (- lamb * L)
aux2 = np.e ** (lamb * L)
denominator = aux1 - aux2
A = ((Ta - Tinf) * aux1 - (Tb - Tinf)) / denominator
B = ((Tb - Tinf) - (Ta - Tinf) * aux2) / denominator

X1 = [T(Tinf, A, B, lamb, x) for x in t]

with open('output.json') as file:
    data = json.load(file)

X2 = data['x']

print(np.array(X1).reshape((len(X1), 1)))
print(np.array(X2).reshape((len(X2), 1)))

plt.figure(constrained_layout=True)
plt.plot(t, X1, label='Solução analítica')
plt.plot(t, X2, label='Diferenças finitas')
plt.legend()
plt.show()
