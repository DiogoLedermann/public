import matplotlib.pyplot as plt

d = [0.2, 0.4, 0.6, 0.8, 1, 1.2, 1.4, 1.6, 1.8]
v = [250.0, 134.0, 73.67, 34.03, 0.415, -33.12, -72.48, -132.1, -245.8]

x = [0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95, 1,
     1.05, 1.1, 1.15, 1.2, 1.25, 1.3, 1.35, 1.4, 1.45, 1.5, 1.55, 1.6, 1.65, 1.7, 1.75, 1.8, 1.85, 1.9, 1.95]

y = [489, 365, 301.3, 250.0, 211.2, 180.4, 155.2, 134.0, 115.9, 100.1, 86.16, 73.67, 63.53, 51.89, 43.23, 34.03, 25.26,
     16.81, 8.559, 0.415, -7.725, -15.96, -24.39 -33.12, -42.28, -51.99, -62.44, -72.48, -84.96, -98.65, -114.2, -132.1,
     -153, -177.7, -207.9, -245.8, -295.8, -367.2, -481.6]

print(len(x))
print(len(y))
plt.subplots(constrained_layout=True)
plt.title('Potencial elétrico entre linhas de cargas', fontsize=30)
plt.xlabel('Distância (m)', fontsize=20)
plt.ylabel('Potencial (v)', fontsize=20)
plt.grid()
plt.scatter(d, v, color='black')
plt.plot(x, y)
plt.show()
