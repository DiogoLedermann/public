from numpy.random import random, randint

candidatos = ['Alejadinho', 'Beethoven', 'Camões']
total = [0, 0, 0]
brancos = 0

eleitores = 10_000

# Eleição honesta
print('Zerésima')
print(total)
for i in range(eleitores):
    # print(f'Eleitor {i+1} votando')
    if random() < 0.1:
        brancos += 1
        print(f'Voto registrado em branco')
    else:
        voto = randint(0, 3)
        total[voto] += 1
        print(f'Voto registrado no candidato {candidatos[voto]}')
    print(total)

max = 0
eleito = None
for i, votos in enumerate(total):
    if votos > max:
        max = votos
        eleito = candidatos[i]
print(f'({total[0]} + {total[1]} + {total[2]}) + ({brancos}) = {sum(total)} votos válidos + {brancos} votos em '
      f'branco = {sum(total) + brancos}')
print(f'O candidato {eleito} foi eleito!')
print()
print()
print()
print()
print()


total = [0, 0, 0]
brancos = 0
# Eleição Fraudulenta
print('Zerésima')
print(total)
for i in range(eleitores):
    # print(f'Eleitor {i+1} votando')
    if random() < 0.1:
        brancos += 1
        print(f'Voto registrado em branco')
    else:
        voto = randint(0, 3)
        if voto == 0:
            total[voto] += 1
        else:
            if random() < 0.98:
                total[voto] += 1
            else:
                total[0] += 1
        print(f'Voto registrado no candidato {candidatos[voto]}')
    print(total)

max = 0
eleito = None
for i, votos in enumerate(total):
    if votos > max:
        max = votos
        eleito = candidatos[i]
print(f'({total[0]} + {total[1]} + {total[2]}) + ({brancos}) = {sum(total)} votos válidos + {brancos} votos em '
      f'branco = {sum(total) + brancos} votos')
print(f'O candidato {eleito} foi eleito!')
print()
print()
print()
print()
print()


# Eleição fraudulente 2
print('Zerésima')
print(total)
for i in range(eleitores):
    # print(f'Eleitor {i+1} votando')
    if random() < 0.1:
        brancos += 1
        print(f'Voto registrado em branco')
    else:
        voto = randint(0, 3)
        print(f'Voto registrado no candidato {candidatos[voto]}')

validos = int((randint(8800, 9300) / 10000) * eleitores)
brancos = int(eleitores - validos)
a = round((randint(41, 50) / 100) * validos)
bc = validos - a
b = round(randint(60, 66) / 100 * bc)
c = int(bc - b)
total = [a, b, c]


max = 0
eleito = None
for i, votos in enumerate(total):
    if votos > max:
        max = votos
        eleito = candidatos[i]
print(f'({total[0]} + {total[1]} + {total[2]}) + ({brancos}) = {validos} votos válidos + {brancos} votos em '
      f'branco = {validos + brancos} votos')
print(f'O candidato {eleito} foi eleito!')
