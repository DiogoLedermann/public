from math import *
from matplotlib import pyplot as plt
import cartopy.crs as ccrs


def calcula_latitude_ponto_intermediario(L1, lambda1, L2, lambda2, lambdai):
    return atan((tan(L2) * sin(lambdai - lambda1) - tan(L1) * sin(lambdai - lambda2)) / sin(lambda2 - lambda1))


def transforma_para_grau_decimal(grau_formatado):
    g, m, s = grau_formatado.split()
    grau = int(g)
    minuto = int(m)
    segundo = int(s)

    if grau > 0:
        segundo_em_decimal = segundo / 60
        minuto += segundo_em_decimal

        minuto_em_decimal = minuto / 60
        grau += minuto_em_decimal
    else:
        segundo_em_minuto = segundo / 60
        minuto += segundo_em_minuto

        minuto_em_grau = minuto / 60
        grau -= minuto_em_grau
    return grau


def transforma_para_grau_formatado(grau_decimal):
    grau_decimal_inteiro = trunc(grau_decimal)
    parte_decimal = grau_decimal - trunc(grau_decimal)
    if parte_decimal < 0:
        parte_decimal *= -1

    minuto = parte_decimal * 60
    minuto_redondo = trunc(minuto)
    parte_decimal_minuto = minuto - trunc(minuto)

    segundo = parte_decimal_minuto * 60
    segundo_redondo = segundo

    if parte_decimal > 0:
        parte_decimal *= -1

    if parte_decimal < 0 and grau_decimal_inteiro == 0:
        return f"-{grau_decimal_inteiro:3}° {minuto_redondo:2}' {segundo_redondo:5.3f}''"
    else:
        return f"{grau_decimal_inteiro:3}° {minuto_redondo:2}' {segundo_redondo:5.3f}''"


with open('coordenadasOslo-Vancouver.txt') as arquivo:
    contador_linhas = 0
    for linha in arquivo:
        contador_linhas += 1
        if contador_linhas == 1:
            latitude_inicial_formatada = linha
        if contador_linhas == 2:
            longitude_inicial_formatada = linha
        if contador_linhas == 3:
            latitude_final_formatada = linha
        if contador_linhas == 4:
            longitude_final_formatada = linha


latitude_inicial_em_graus_decimal = transforma_para_grau_decimal(latitude_inicial_formatada)
latitude_inicial = radians(latitude_inicial_em_graus_decimal)


longitude_inicial_em_graus_decimal = transforma_para_grau_decimal(longitude_inicial_formatada)
longitude_inicial_em_graus_inteiro = trunc(longitude_inicial_em_graus_decimal)
longitude_inicial = radians(longitude_inicial_em_graus_decimal)


latitude_final_em_graus_decimal = transforma_para_grau_decimal(latitude_final_formatada)
latitude_final = radians(latitude_final_em_graus_decimal)


longitude_final_em_graus_decimal = transforma_para_grau_decimal(longitude_final_formatada)
longitude_final_em_graus_inteiro = trunc(longitude_final_em_graus_decimal)
longitude_final = radians(longitude_final_em_graus_decimal)


if longitude_final_em_graus_inteiro > longitude_inicial_em_graus_inteiro:
    passo = 1
    longitude_final_em_graus_inteiro += 1
else:
    passo = -1
    longitude_final_em_graus_inteiro -= 1


coordenadas = {}
x_axis = []
y_axis = []

for longitude in range(longitude_inicial_em_graus_inteiro, longitude_final_em_graus_inteiro, passo):

    x_axis.append(longitude)

    longitude_ponto_intermediario_formatada = transforma_para_grau_formatado(longitude)

    longitude_ponto_intermediario = radians(longitude)

    latitude_ponto_intermediario_em_radianos = calcula_latitude_ponto_intermediario(latitude_inicial,
                                                                                    longitude_inicial,
                                                                                    latitude_final,
                                                                                    longitude_final,
                                                                                    longitude_ponto_intermediario)

    latitude_ponto_intermediario_em_graus = degrees(latitude_ponto_intermediario_em_radianos)

    y_axis.append(latitude_ponto_intermediario_em_graus)

    latitude_ponto_intermediario_formatada = transforma_para_grau_formatado(latitude_ponto_intermediario_em_graus)

    coordenadas[longitude_ponto_intermediario_formatada] = latitude_ponto_intermediario_formatada

plt.plot(x_axis, y_axis, 'ro')
plt.title('Rota')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.grid(True)
plt.show()

for i, chave in enumerate(coordenadas):
    print(f'Coordenada {i + 1:3}: Latitude {coordenadas[chave]:18} Longitude {chave}')


