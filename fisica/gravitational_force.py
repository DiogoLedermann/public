import numpy as np
np.set_printoptions(precision=3, suppress=True)

g = 6.674 * 10 ** -11  # Constante gravitacional de Newton
m2 = 3.3  # Massa média de um bebê.


def forcaGravitacional(m1, m2, r):
    return (g * m1 * m2) / (r ** 2)


astros = ['Sol',
          'Lua',
          'Mercúrio',
          'Vênus',
          'Marte',
          'Júpiter',
          'Saturno',
          'Urano',
          'Netuno',
          'Plutão',
          'Alpha Centauri',
          'Obstetra']

massasDosAstros = [1.989 * 10 ** 30,
                   7.36 * 10 ** 22,
                   3.285 * 10 ** 23,
                   4.867 * 10 ** 24,
                   6.39 * 10 ** 23,
                   1.898 * 10 ** 27,
                   5.683 * 10 ** 26,
                   8.681 * 10 ** 25,
                   1.024 * 10 ** 26,
                   1.305 * 10 ** 22,
                   1.1055 * (1.989 * 10 ** 30),
                   70]

distancias = [1.496 * 10 ** 11,
              3.844 * 10 ** 8,
              9.169 * 10 ** 10,
              4.14 * 10 ** 10,
              7.834 * 10 ** 10,
              6.2873 * 10 ** 11,
              1.2798 * 10 ** 12,
              2.72139 * 10 ** 12,
              4.3547 * 10 ** 12,
              5.76392 * 10 ** 12,
              4.100 * 10 ** 13,
              1]

m1 = 5.792 * 10 ** 24
m2 = massasDosAstros[0]
r = distancias[0]
print(forcaGravitacional(m1, m2, r))
m2 = massasDosAstros[1]
r = distancias[1]
print(forcaGravitacional(m1, m2, r))

forcas = np.array([forcaGravitacional(massasDosAstros[i], distancias[i]) for i, astro in enumerate(astros)])
# for i, forca in enumerate(forcas):
#     print(f'{astros[i]:15}: {forca} N')
#     print(f'{astros[i]:15}: {(forcas[i] / forcas[0]) * 100:16.12f} % da influência do sol.')
#     print()
